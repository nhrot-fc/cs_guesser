from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google import generativeai as genai
import os
import json
import random
from .controllers.prompt_controller import PromptController
from .models.quiz_question import QuizQuestion

def index(request):
    """
    Vista principal que renderiza el template con una pregunta generada.
    """
    # Generar una pregunta inicial
    question = generate_question()
    
    # Convertir la pregunta a formato para el template
    question_data = format_question_for_template(question)
    
    # Renderizar el template con los datos
    return render(request, 'quiz.html', {'question': question_data})

def generate_question(topic="Random", subtopic=None, difficulty=3):
    """
    Genera una pregunta utilizando el PromptController y la API de Gemini
    """
    # Configurar la API key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Inicializar el controlador de prompts
    prompt_controller = PromptController()
    
    # Generar el prompt para la API de Gemini
    prompt = prompt_controller.generate_prompt(
        topic=topic, 
        subtopic=subtopic, 
        difficulty=difficulty
    )
    
    # Mostrar el prompt para depuración
    print("\n-------- PROMPT GENERADO --------")
    print(prompt)
    print("--------------------------------\n")
    
    # Inicializar el modelo Gemini 2.0 Flash
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    try:
        # Generar contenido
        response = model.generate_content(prompt)
        
        print("\n-------- RESPUESTA RAW --------")
        print(response)
        print("--------------------------------\n")
        
        # La respuesta de la API no es directamente JSON
        if response and hasattr(response, 'text'):
            response_text = response.text.strip()
            # Intentar extraer JSON si está envuelto en marcadores de código
            if response_text.startswith("```json") and response_text.endswith("```"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```") and response_text.endswith("```"):
                response_text = response_text[3:-3].strip()
                
            # Intentar parsear la respuesta JSON
            try:
                response_json = json.loads(response_text)
                
                # Mostrar la respuesta para depuración
                print("\n-------- RESPUESTA PARSEADA --------")
                print(json.dumps(response_json, indent=2, ensure_ascii=False))
                print("--------------------------------\n")
                
                # Validar el formato de la respuesta
                if prompt_controller.validate_response_format(response_json):
                    return response_json
                else:
                    print("Formato de respuesta inválido:", response_json)
                    raise ValueError("Formato de respuesta inválido")
            except json.JSONDecodeError as json_err:
                print("Error al decodificar JSON:", json_err)
                print("Texto recibido:", response_text)
                raise ValueError(f"Error al parsear JSON: {str(json_err)}")
        else:
            raise ValueError("No se recibió respuesta del modelo")
            
    except Exception as e:
        # En caso de error, devolver una pregunta predefinida
        print(f"Error al generar pregunta: {str(e)}")
        return get_fallback_question()

def get_fallback_question():
    """Devuelve una pregunta predefinida en caso de error"""
    return {
        "question": "¿Qué estructura de datos utiliza el principio LIFO?",
        "clues": [
            "Es una estructura fundamental en ciencias de la computación",
            "Se utiliza frecuentemente en la implementación de algoritmos recursivos",
            "Es opuesta a una estructura FIFO",
            "Se utiliza para mantener un historial de operaciones",
            "El último elemento insertado es el primero en ser extraído"
        ],
        "type": "unique_answer",
        "options": [
            {"label": "Cola (Queue)", "answer": False},
            {"label": "Pila (Stack)", "answer": True},
            {"label": "Lista enlazada (Linked List)", "answer": False},
            {"label": "Árbol (Tree)", "answer": False},
            {"label": "Tabla hash (Hash Table)", "answer": False}
        ],
        "metadata": {
            "topic": "Estructuras de Datos",
            "subtopic": "Estructuras Lineales",
            "difficulty": 2,
            "tags": ["data structures", "stack", "LIFO"]
        },
        "summary": "Una pila (stack) es una estructura de datos que sigue el principio LIFO (Last In First Out), donde el último elemento insertado es el primero en ser extraído."
    }

def format_question_for_template(question_data):
    """
    Formatea los datos de la pregunta para el template
    """
    # Extraer las opciones como texto plano
    options = [option.get('label', '') for option in question_data.get('options', [])]
    
    # Encontrar el índice de la respuesta correcta
    try:
        correct_index = next(
            (i for i, option in enumerate(question_data.get('options', [])) 
             if option.get('answer', False)), 
            0
        )
    except Exception:
        # Si no se encuentra respuesta correcta, usar la primera opción
        correct_index = 0
        print("ADVERTENCIA: No se encontró una respuesta correcta en las opciones")
    
    # Mapear nivel de dificultad numérico a texto
    difficulty_map = {
        1: "Fácil",
        2: "Fácil",
        3: "Medio",
        4: "Difícil",
        5: "Difícil"
    }
    
    # Obtener metadata
    metadata = question_data.get('metadata', {})
    difficulty_level = metadata.get('difficulty', 3)
    
    # Formatear para el template
    formatted_question = {
        'id': random.randint(1000, 9999),  # ID aleatorio para la pregunta
        'question_text': question_data.get('question', 'Pregunta no disponible'),
        'options': options if options else ["Opción A", "Opción B", "Opción C", "Opción D"],
        'correct_index': correct_index,
        'explanation': question_data.get('summary', 'No hay explicación disponible.'),
        'general_topic': metadata.get('topic', 'General'),
        'specific_topic': metadata.get('subtopic', 'General'),
        'difficulty': difficulty_map.get(difficulty_level, 'Medio'),
        'clues': question_data.get('clues', ["No hay pistas disponibles"])
    }
    
    # Verificar datos y registrar para depuración
    print(f"Pregunta formateada ID #{formatted_question['id']}:")
    print(f"Tema: {formatted_question['general_topic']} > {formatted_question['specific_topic']}")
    print(f"Opciones: {len(formatted_question['options'])}, Correcta: {correct_index}")
    
    return formatted_question

@csrf_exempt
def next_question(request):
    """Endpoint para obtener la siguiente pregunta"""
    if request.method == 'POST':
        try:
            # Generar nueva pregunta
            question = generate_question()
            
            # Formatear para el template
            formatted_question = format_question_for_template(question)
            
            return JsonResponse(formatted_question)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def gemini_request(request):
    """Endpoint original para pruebas directas de la API Gemini"""
    # Configure the API key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # For Gemini 2.0 Flash
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Generate content
    response = model.generate_content("Write a poem about AI")
    
    # Handle the response
    if response and hasattr(response, 'text'):
        return JsonResponse({"response": response.text})
    else:
        return JsonResponse({"error": "Failed to generate response"}, status=500)
