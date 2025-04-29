# gemini_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging

from .controllers.question_controller import GeminiQuestionController

# Configure logging to show debug logs
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize controller correctly without passing API key (it reads from env)
controller = GeminiQuestionController()

def index(request):
    """
    Render the quiz page
    """
    try:
        # Generate a single quiz question for initial render
        questions = controller.generate_questions(count=1)
        question_data = questions[0].to_dict() if questions else None
    except Exception as e:
        logger.error(f"Error generating initial question: {e}", exc_info=True)
        question_data = None
    return render(request, 'quiz.html', {'question': question_data})

@require_http_methods(["GET"])
def check(request):
    """
    Generate quiz questions based on the 'cant' parameter
    and return them as JSON
    """
    try:
        # Get the count parameter, default to 5 if not provided
        count = int(request.GET.get('cant', 5))
        
        logger.info(f"Generating {count} quiz questions")
        
        # Generate questions using the controller
        questions = controller.generate_questions(count=count)
        
        if not questions:
            logger.error("Failed to generate questions")
            return JsonResponse({"error": "Failed to generate questions"}, status=500)
        
        # Convert questions to dictionary using to_dict method for proper JSON serialization
        questions_data = [q.to_dict() for q in questions]
        
        logger.info(f"Successfully generated {len(questions)} questions")
        return JsonResponse({"questions": questions_data})
        
    except Exception as e:
        logger.error(f"Error in check endpoint: {str(e)}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)
