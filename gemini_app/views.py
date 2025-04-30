# gemini_app/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
import logging
import json
import uuid
import threading
from dataclasses import dataclass, asdict

from .controllers.question_controller import GeminiQuestionController

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Metrics:
    total_answered: int = 0
    correct_answers: int = 0
    current_streak: int = 0
    max_streak: int = 0

    @property
    def accuracy(self):
        return round((self.correct_answers / self.total_answered) * 100) if self.total_answered else 0

    def record_answer(self, is_correct: bool):
        self.total_answered += 1
        if is_correct:
            self.correct_answers += 1
            self.current_streak += 1
            if self.current_streak > self.max_streak:
                self.max_streak = self.current_streak
        else:
            self.current_streak = 0

    def to_dict(self):
        data = asdict(self)
        data['accuracy'] = self.accuracy
        return data

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            total_answered=data.get('total_answered', 0),
            correct_answers=data.get('correct_answers', 0),
            current_streak=data.get('current_streak', 0),
            max_streak=data.get('max_streak', 0),
        )


controller = GeminiQuestionController()
DEFAULT_BATCH_SIZE = 5


# Métodos auxiliares para manejar la generación y gestión de preguntas
def _ensure_metrics_initialized(request):
    """
    Garantiza que las métricas estén inicializadas en la sesión.
    
    Args:
        request: HttpRequest de Django con la sesión activa
    """
    if 'metrics' not in request.session:
        request.session['metrics'] = Metrics().to_dict()
        request.session.modified = True


def _get_current_question(request):
    """
    Obtiene la pregunta actual basada en el índice de la sesión.
    
    Args:
        request: HttpRequest de Django con la sesión activa
        
    Returns:
        dict: La pregunta actual o None si no hay preguntas disponibles
    """
    questions = request.session.get('questions', [])
    idx = request.session.get('current_question_index', 0)
    
    if questions and 0 <= idx < len(questions):
        return questions[idx]
    return None


def _needs_new_batch(request):
    """
    Determina si se necesita generar un nuevo batch de preguntas.
    
    Args:
        request: HttpRequest de Django con la sesión activa
        
    Returns:
        bool: True si se necesita un nuevo batch, False en caso contrario
    """
    questions = request.session.get('questions', [])
    idx = request.session.get('current_question_index', 0)
    
    # Necesitamos un nuevo batch si:
    # 1. No hay preguntas
    # 2. El índice está fuera de rango
    return not questions or idx >= len(questions)


def _is_generation_in_progress(request):
    """
    Verifica si hay una generación de preguntas en progreso.
    
    Args:
        request: HttpRequest de Django con la sesión activa
        
    Returns:
        bool: True si hay una generación en progreso, False en caso contrario
    """
    task_id = request.session.get('generation_task_id')
    return (request.session.get('generation_in_progress', False) and 
            task_id and 
            controller.is_generation_in_progress(task_id))


def _get_generation_status(request):
    """
    Obtiene el estado actual de la generación de preguntas.
    
    Args:
        request: HttpRequest de Django con la sesión activa
        
    Returns:
        dict: Diccionario con el estado de la generación
    """
    task_id = request.session.get('generation_task_id')
    if not task_id:
        return {
            'status': 'unknown',
            'message': 'No generation task in progress'
        }
    return controller.get_generation_status(task_id)


def _reset_batch(request):
    """
    Resetea el batch actual y prepara para uno nuevo.
    
    Args:
        request: HttpRequest de Django con la sesión activa
    """
    request.session['questions'] = []
    request.session['current_question_index'] = 0
    request.session.modified = True
    logger.info("Reset batch and prepared for new generation")


def _start_question_generation(request):
    """
    Inicia la generación de preguntas en un thread separado.
    
    Args:
        request: HttpRequest de Django con la sesión activa
    """
    # Generar un nuevo ID de tarea y almacenarlo en la sesión
    task_id = str(uuid.uuid4())
    request.session['generation_task_id'] = task_id
    request.session['generation_in_progress'] = True
    request.session.modified = True
    
    # Iniciar la generación de preguntas en un hilo en segundo plano
    def generate_questions_task():
        try:
            new_questions = controller.generate_questions(count=DEFAULT_BATCH_SIZE, task_id=task_id)
            if new_questions:
                # Actualizar la sesión con nuevas preguntas
                request.session['questions'] = [q.to_dict() for q in new_questions]
                request.session['current_question_index'] = 0
                request.session['generation_in_progress'] = False
                request.session.modified = True
                logger.info(f"Generated batch of {len(new_questions)} questions successfully")
            else:
                logger.error("Failed to generate questions")
                request.session['generation_error'] = "Failed to generate questions"
                request.session['generation_in_progress'] = False
                request.session.modified = True
        except Exception as e:
            logger.error(f"Error in question generation thread: {e}", exc_info=True)
            request.session['generation_error'] = str(e)
            request.session['generation_in_progress'] = False
            request.session.modified = True
    
    # Iniciar un nuevo hilo solo si vamos a generar preguntas
    threading.Thread(target=generate_questions_task, daemon=True).start()
    logger.info(f"Started question generation with task_id: {task_id}")


def _init_quiz(request):
    """
    Inicializa o actualiza el estado del quiz según sea necesario.
    
    Args:
        request: HttpRequest de Django con la sesión activa
    """
    # Inicializar métricas si es necesario
    _ensure_metrics_initialized(request)
    
    # Verificar si necesitamos generar nuevas preguntas
    if not _needs_new_batch(request):
        return
    
    # Si ya estamos generando preguntas, solo retornar
    if _is_generation_in_progress(request):
        return
    
    # Resetear el batch si tenemos preguntas pero el índice está fuera de rango
    questions = request.session.get('questions', [])
    idx = request.session.get('current_question_index', 0)
    if questions and idx >= len(questions):
        _reset_batch(request)
    
    # Iniciar la generación de nuevas preguntas
    _start_question_generation(request)


@ensure_csrf_cookie
def index(request):
    try:
        # Manejo especial para solicitudes HEAD para evitar disparar la generación de preguntas
        if request.method == 'HEAD':
            return render(request, 'base.html', {
                'loading': True,
                'message': 'Health check ping received'
            })
            
        # Inicializar el estado del quiz
        _init_quiz(request)
        
        # Resetear banderas para esta carga de página
        request.session['increment_pending'] = False
        request.session['answer_recorded'] = False
        request.session.modified = True
        
        # Verificar si aún estamos generando preguntas
        if _is_generation_in_progress(request):
            status = _get_generation_status(request)
            # Renderizar una página de carga con información de estado
            return render(request, 'quiz.html', {
                'loading': True,
                'status': status,
                'metrics': request.session.get('metrics', {}),
            })
                
        # Verificar si hubo un error durante la generación
        if 'generation_error' in request.session:
            error = request.session.pop('generation_error')
            return render(request, 'error.html', {'error': error})
            
        # Si tenemos preguntas, renderizar la página del quiz
        current_question = _get_current_question(request)
        if current_question:
            metrics = request.session.get('metrics', {})
            return render(request, 'quiz.html', {
                'question': current_question,
                'metrics': metrics,
                'question_number': request.session.get('current_question_index', 0),
                'total_questions': len(request.session.get('questions', []))
            })
            
        # Si llegamos aquí, aún estamos esperando preguntas
        return render(request, 'quiz.html', {
            'loading': True,
            'message': 'Preparing your quiz questions...',
            'metrics': request.session.get('metrics', {})
        })
            
    except Exception as e:
        logger.error(f"Error rendering quiz: {e}", exc_info=True)
        logger.debug(f"Session data: {request.session.items()}")
        return render(request, 'error.html', {'error': str(e)})


@require_http_methods(["GET"])
def check_generation_status(request):
    """Endpoint para verificar el estado de la generación de preguntas"""
    status = _get_generation_status(request)
    
    # Si la generación está completa, actualizar la sesión
    if status.get('status') == 'completed' and status.get('questions'):
        request.session['questions'] = status.get('questions')
        request.session['current_question_index'] = 0
        request.session['generation_in_progress'] = False
        request.session.modified = True
        
    # Si la generación falló, registrar el error
    elif status.get('status') == 'failed':
        request.session['generation_error'] = status.get('message', 'Unknown error')
        request.session['generation_in_progress'] = False
        request.session.modified = True
        
    return JsonResponse(status)


@require_http_methods(["POST"])
def submit_answer(request):
    try:
        # Verificar si ya se registró esta respuesta para evitar duplicación
        if request.session.get('answer_recorded', False):
            # Si ya se registró, simplemente devolver los datos actuales
            return JsonResponse({'success': True, 'metrics': request.session.get('metrics', {})})
            
        data = json.loads(request.body)
        is_correct = data.get('is_correct', False)
        # Utilizar la clase Metrics para actualizar las métricas de la sesión
        metrics_obj = Metrics.from_dict(request.session.get('metrics', {}))
        metrics_obj.record_answer(is_correct)
        updated_metrics = metrics_obj.to_dict()
        request.session['metrics'] = updated_metrics
        
        # Marcar que la respuesta ha sido registrada
        request.session['answer_recorded'] = True
        request.session.modified = True
        
        return JsonResponse({'success': True, 'metrics': updated_metrics})
    except Exception as e:
        logger.error(f"Error processing answer: {e}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["GET"])
def next_question(request):
    logger.info(f"NEXT QUESTION - Current question index: {request.session.get('current_question_index', 0)}")
    
    # Verificar si la bandera de incremento está configurada para evitar incrementos dobles
    if not request.session.get('increment_pending', False):
        # Avanzar a la siguiente pregunta
        current_idx = request.session.get('current_question_index', 0)
        request.session['current_question_index'] = current_idx + 1
        # Establecer bandera para indicar que hemos incrementado
        request.session['increment_pending'] = True
        logger.info(f"Incremented question index to: {current_idx + 1}")
    
    # Resetear la bandera answer_recorded para la nueva pregunta
    request.session['answer_recorded'] = False
    request.session.modified = True
    
    # Re-inicializar el quiz si es necesario (batch agotado)
    _init_quiz(request)
    
    # Verificar si aún estamos generando preguntas
    if _is_generation_in_progress(request):
        status = _get_generation_status(request)
        return JsonResponse({
            'loading': True,
            'status': status
        })
    
    # Si las preguntas están listas, devolverlas
    current_question = _get_current_question(request)
    if current_question:
        idx = request.session.get('current_question_index', 0)
        metrics = request.session.get('metrics', {})
        return JsonResponse({
            'question': current_question,
            'metrics': metrics,
            'question_number': idx,
            'total_questions': len(request.session.get('questions', []))
        })
    
    # Si aún no tenemos preguntas
    return JsonResponse({
        'loading': True,
        'message': 'Preparing your next question...'
    })


@require_http_methods(["GET"])
def get_metrics(request):
    return JsonResponse({'metrics': request.session.get('metrics', {})})


@require_http_methods(["POST"])
def reset_metrics(request):
    # Resetear métricas de sesión usando la clase Metrics
    request.session['metrics'] = Metrics().to_dict()
    return JsonResponse({'success': True})


@require_http_methods(["GET"])
def clear_session(request):
    request.session.flush()
    return redirect('index')
