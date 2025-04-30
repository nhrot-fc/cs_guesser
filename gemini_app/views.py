# gemini_app/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
import logging
import json
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


def _init_quiz(request):
    # Initialize metrics and fetch a new batch if needed
    if 'metrics' not in request.session:
        request.session['metrics'] = Metrics().to_dict()
    questions = request.session.get('questions', [])
    idx = request.session.get('current_question_index', 0)
    if not questions or idx >= len(questions):
        new_questions = controller.generate_questions(count=DEFAULT_BATCH_SIZE)
        if new_questions:
            request.session['questions'] = [q.to_dict() for q in new_questions]
            request.session['current_question_index'] = 0
        else:
            logger.error("Failed to generate questions")
            raise Exception("Failed to generate questions")


@ensure_csrf_cookie
def index(request):
    try:
        _init_quiz(request)
        
        # Reset the increment_pending flag when rendering a question page
        request.session['increment_pending'] = False
        request.session.modified = True
        
        q = request.session['questions'][request.session['current_question_index']]
        metrics = request.session['metrics']
        return render(request, 'quiz.html', {
            'question': q,
            'metrics': metrics,
            'question_number': request.session['current_question_index'],
            'total_questions': len(request.session['questions'])
        })
    except Exception as e:
        logger.error(f"Error rendering quiz: {e}", exc_info=True)
        return render(request, 'error.html', {'error': str(e)})


@require_http_methods(["POST"])
def submit_answer(request):
    try:
        data = json.loads(request.body)
        is_correct = data.get('is_correct', False)
        # Use Metrics dataclass for updating session metrics
        metrics_obj = Metrics.from_dict(request.session.get('metrics', {}))
        metrics_obj.record_answer(is_correct)
        updated_metrics = metrics_obj.to_dict()
        request.session['metrics'] = updated_metrics
        return JsonResponse({'success': True, 'metrics': updated_metrics})
    except Exception as e:
        logger.error(f"Error processing answer: {e}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["GET"])
def next_question(request):
    print(f"NEXT QUESTION - Current question index: {request.session.get('current_question_index', 0)}")
    
    # Check if the increment flag is set to avoid double increments
    if not request.session.get('increment_pending', False):
        # Move to next question
        request.session['current_question_index'] = request.session.get('current_question_index', 0) + 1
        # Set flag to indicate we've incremented
        request.session['increment_pending'] = True
    
    # Save the session to ensure changes are persisted
    request.session.modified = True
    
    # Re-init quiz if needed (batch exhausted)
    _init_quiz(request)
    
    q = request.session['questions'][request.session['current_question_index']]
    metrics = request.session['metrics']
    return JsonResponse({
        'question': q,
        'metrics': metrics,
        'question_number': request.session['current_question_index'],
        'total_questions': len(request.session['questions'])
    })


@require_http_methods(["GET"])
def get_metrics(request):
    return JsonResponse({'metrics': request.session.get('metrics', {})})


@require_http_methods(["POST"])
def reset_metrics(request):
    # Reset session metrics using Metrics dataclass
    request.session['metrics'] = Metrics().to_dict()
    return JsonResponse({'success': True})


@require_http_methods(["GET"])
def clear_session(request):
    request.session.flush()
    return redirect('index')
