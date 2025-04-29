from django.shortcuts import render
from django.http import JsonResponse
from google import generativeai as genai
import os
import random
import json
import re
from enum import Enum
from .constants import (
    ResponseType, 
    QuestionType,
    ReferenceType,
    QuizQuestion,
    Option,
    Reference,
    QuestionMetadata,
    PROMPT_BUILDER
)

"""GEMINI API REQUEST EXAMPLE:

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=GEMINI_API_KEY" \
-H 'Content-Type: application/json' \
-X POST \
-d '{
  "contents": [{
    "parts":[{"text": "Explain how AI works"}]
    }]
   }'
"""

def gemini_request(request):
    # Configure the API key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # For Gemini 2.0 Flash
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Get request parameters or use defaults
    topic = request.GET.get('topic', random.choice(list(SYLLABUS["core_topics"].keys())))
    subtopic = request.GET.get('subtopic', None)
    
    # If topic is provided but subtopic isn't, randomly select a subtopic from that topic
    if topic in SYLLABUS["core_topics"] and not subtopic:
        subtopic = random.choice(SYLLABUS["core_topics"][topic])
    
    # Get difficulty level (1-5) with a default of INTERMEDIATE (3)
    difficulty_param = request.GET.get('difficulty', 3)
    try:
        difficulty_param = int(difficulty_param)
        if difficulty_param < 1 or difficulty_param > 5:
            raise ValueError("Difficulty must be between 1 and 5")
    except ValueError:
        return JsonResponse({"error": "Invalid difficulty level"}, status=400)
    
    # Generate prompt using the PROMPT_BUILDER from constants
    prompt = PROMPT_BUILDER.build_prompt(
        topic=topic, 
        subtopic=subtopic, 
        difficulty=difficulty_param,
        include_features=["core", "references"]
    )
    
    # Generate content
    try:
        response = model.generate_content(prompt)
        
        # Handle the response
        if response and hasattr(response, 'text'):
            # Extract JSON from the response text
            json_text = response.text
            json_match = re.search(r'```(?:json)?(.*?)```', json_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(1).strip()
            
            try:
                # Parse the JSON response
                raw_quiz_data = json.loads(json_text)
                
                # Convert raw JSON to QuizQuestion object
                try:
                    quiz_question = QuizQuestion.from_dict(raw_quiz_data)
                    
                    # If certain fields are missing, enrich the data
                    if not hasattr(quiz_question, 'metadata') or not quiz_question.metadata:
                        quiz_question.metadata = QuestionMetadata(
                            topic=topic,
                            subtopic=subtopic if subtopic else "General",
                            difficulty=difficulty_param,
                            tags=[]
                        )
                    
                    # If options are missing, generate them
                    if not quiz_question.options or len(quiz_question.options) == 0:
                        correct_answer = extract_correct_answer(raw_quiz_data)
                        if correct_answer:
                            quiz_question.options = generate_options(correct_answer, topic, quiz_question.type)
                    
                    # Convert back to dictionary for JSON response
                    return JsonResponse(quiz_question.to_dict())
                except Exception as e:
                    # If QuizQuestion creation fails, return the raw data
                    return JsonResponse(raw_quiz_data)
                
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw text
                return JsonResponse({"error": "Failed to parse JSON", "raw_response": response.text}, status=500)
        else:
            return JsonResponse({"error": "Failed to generate response"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def extract_correct_answer(quiz_data):
    """Extract the correct answer from the quiz data"""
    # Check if there's a direct answer field (old format)
    if "answer" in quiz_data:
        return quiz_data["answer"]
    
    # Check in options for the one marked as answer=true (new format)
    if "options" in quiz_data:
        for option in quiz_data["options"]:
            if option.get("answer", False):
                return option.get("label")
    
    return None

def generate_options(correct_answer, topic, question_type=ResponseType.UNIQUE_ANSWER.value):
    """Generate options with the Option dataclass"""
    # These are topic-categorized distractors for more contextually relevant options
    distractor_options = {
        "Algoritmos": [
            "Quick Sort", "Merge Sort", "Heap Sort", "Bubble Sort", "Insertion Sort",
            "Binary Search", "Linear Search", "Hash Table", "B-Tree", "AVL Tree",
            "O(n)", "O(log n)", "O(n²)", "O(1)", "O(n log n)"
        ],
        "Sistemas": [
            "Process Scheduling", "Memory Management", "File System", "Deadlock Prevention", 
            "Cache Coherence", "Virtual Memory", "Paging", "RAID", "Thread Synchronization",
            "Mutex", "Semaphore", "Monitor", "Pipeline", "Superscalar Architecture"
        ],
        "IA/ML": [
            "Decision Tree", "Random Forest", "Gradient Descent", "Backpropagation",
            "Convolutional Neural Network", "Recurrent Neural Network", "LSTM", "Transformer",
            "Reinforcement Learning", "Supervised Learning", "Unsupervised Learning",
            "K-means Clustering", "Principal Component Analysis", "Support Vector Machine"
        ],
        # Default fallback options if topic isn't recognized
        "default": [
            "Binary Search Tree", "Queue", "Stack", "Heap", "Linked List",
            "O(n)", "O(log n)", "O(n²)", "O(1)", "O(n log n)",
            "SQL", "NoSQL", "MongoDB", "PostgreSQL", "Redis",
            "Breadth-First Search", "Depth-First Search", "Dijkstra's Algorithm", 
            "A* Algorithm", "Bellman-Ford Algorithm"
        ]
    }
    
    # Get the appropriate distractors for the topic
    distractors = distractor_options.get(topic, distractor_options["default"])
    
    # For multiple answers type, we need to format differently
    is_multiple = question_type == ResponseType.MULTIPLE_ANSWERS.value
    
    # Create a list of option objects according to the schema
    options = [Option(label=correct_answer, answer=True)]
    
    # For multiple answers, potentially make more than one answer correct
    if is_multiple and random.random() > 0.5:
        # Add another correct answer 25% of the time for multiple answer questions
        options.append(Option(label=f"Alternative correct answer for {correct_answer}", answer=True))
    
    # Add distractors (incorrect options)
    num_distractors = 4 if not is_multiple else 3
    while len(options) < num_distractors + 1:
        distractor = random.choice(distractors)
        # Check if this distractor is already in our options
        if not any(option.label == distractor for option in options):
            options.append(Option(label=distractor, answer=False))
    
    # Shuffle the options
    random.shuffle(options)
    return options