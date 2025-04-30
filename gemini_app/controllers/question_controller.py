"""
Controller for generating questions using Gemini API
"""
import json
import logging
import threading
import time
from google import genai
from typing import List, Optional, Dict
from ..models.quiz_question import QuizQuestion
from ..models.prompt_template import PromptTemplate
import os
import re

# Configure logging for the controller
logger = logging.getLogger(__name__)

class GeminiQuestionController:
    def __init__(self):
        """
        Initialize the GeminiQuestionController with the provided API key.
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("GOOGLE_API_KEY environment variable not set")
            raise ValueError("GOOGLE_API_KEY environment variable not set")
            
        try:
            self.client = genai.Client(api_key=api_key)
            logger.info("Gemini API client initialized successfully")
        except Exception as e:
            logger.error(f"Gemini API client initialization failed: {e}")
            raise ValueError(f"Gemini API client initialization failed: {e}")
        
        # Track generation tasks in progress to avoid duplicates
        self._generation_tasks = {}
        self._lock = threading.Lock()
        
    def is_generation_in_progress(self, task_id: str) -> bool:
        """
        Check if a generation task is already in progress
        
        Args:
            task_id: Unique identifier for the generation task
            
        Returns:
            True if the task is in progress, False otherwise
        """
        with self._lock:
            return task_id in self._generation_tasks
            
    def get_generation_status(self, task_id: str) -> Dict:
        """
        Get the status of a generation task
        
        Args:
            task_id: Unique identifier for the generation task
            
        Returns:
            Dict with status information
        """
        with self._lock:
            if task_id not in self._generation_tasks:
                return {
                    "status": "not_found",
                    "message": "No generation task found with this ID"
                }
            
            task_info = self._generation_tasks[task_id]
            return {
                "status": task_info.get("status", "unknown"),
                "started_at": task_info.get("started_at", 0),
                "questions": task_info.get("questions", []),
                "message": task_info.get("message", ""),
                "progress": task_info.get("progress", 0)
            }
        
    def generate_questions(
        self, 
        count: int,
        task_id: Optional[str] = None
    ) -> Optional[List[QuizQuestion]]:
        """
        Generate quiz questions using the Gemini API.
        
        Args:
            count: Number of questions to generate
            task_id: Optional unique identifier for tracking this generation task
            
        Returns:
            List of QuizQuestion objects or None if an error occurs
        """
        # If no task_id provided, create one
        task_id = task_id or f"gen_{int(time.time())}"
        
        # Check if this task is already in progress
        with self._lock:
            if task_id in self._generation_tasks:
                logger.info(f"Generation task {task_id} already in progress")
                return None
            
            # Register this task as in progress
            self._generation_tasks[task_id] = {
                "status": "in_progress",
                "started_at": time.time(),
                "progress": 0,
                "message": "Initializing question generation..."
            }
        
        try:
            with self._lock:
                self._generation_tasks[task_id]["message"] = "Sending request to Gemini API..."
                self._generation_tasks[task_id]["progress"] = 10
            
            prompt = PromptTemplate.get_prompt_template(count=count)
            logger.info(f"Sending request to Gemini API for {count} questions")
            
            with self._lock:
                self._generation_tasks[task_id]["message"] = "Waiting for Gemini API response..."
                self._generation_tasks[task_id]["progress"] = 30
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            
            with self._lock:
                self._generation_tasks[task_id]["message"] = "Processing Gemini response..."
                self._generation_tasks[task_id]["progress"] = 70
            
            # Extract the text content from the response
            if hasattr(response, 'text'):
                response_text = response.text or ""
            else:
                response_text = str(response)
                logger.warning(f"Response from Gemini API doesn't have text attribute")
                
            with self._lock:
                self._generation_tasks[task_id]["message"] = "Parsing questions..."
                self._generation_tasks[task_id]["progress"] = 90
                
            questions = self._parse_response(response_text)
            logger.info(f"Generated {len(questions)} questions")
            
            with self._lock:
                self._generation_tasks[task_id]["status"] = "completed"
                self._generation_tasks[task_id]["questions"] = [q.to_dict() for q in questions]
                self._generation_tasks[task_id]["message"] = "Questions generated successfully"
                self._generation_tasks[task_id]["progress"] = 100
            
            return questions
            
        except Exception as e:
            logger.error(f"Error during API call: {e}")
            with self._lock:
                self._generation_tasks[task_id]["status"] = "failed"
                self._generation_tasks[task_id]["message"] = f"Error: {str(e)}"
            return None
        finally:
            # Keep the task info for status checks, but clean up after some time
            def cleanup_task():
                time.sleep(300)  # Keep task info for 5 minutes
                with self._lock:
                    if task_id in self._generation_tasks:
                        del self._generation_tasks[task_id]
            
            threading.Thread(target=cleanup_task, daemon=True).start()
    
    def _parse_response(self, response_text: str) -> List[QuizQuestion]:
        """
        Parse the response from the Gemini API and convert it into a list of QuizQuestion objects.
        
        Args:
            response_text: The text response from the Gemini API
            
        Returns:
            List of QuizQuestion objects
        """
        questions = []
        try:
            # Try to find JSON content in the response
            # Sometimes the API might return markdown or other formatting
            response_text = self._extract_json_from_text(response_text)
            
            data = json.loads(response_text)
            
            # Handle different possible JSON structures
            if isinstance(data, list):
                # If the response is a list of questions
                for item in data:
                    question = QuizQuestion.from_dict(item)
                    if question.options:
                        questions.append(question)
                    else:
                        logger.warning(f"Question missing options")
            elif isinstance(data, dict):
                if 'questions' in data:
                    # If the response has a 'questions' key with a list
                    for item in data.get('questions', []):
                        question = QuizQuestion.from_dict(item)
                        questions.append(question)
                else:
                    # If the response is a single question
                    question = QuizQuestion.from_dict(data)
                    if question.options:
                        questions.append(question)
                    else:
                        logger.warning(f"Question missing options")
                    
            return questions
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return []
        except KeyError as e:
            logger.error(f"Key error in response data: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error while parsing response: {e}")
            return []
    
    def _extract_json_from_text(self, text: str) -> str:
        """
        Extract JSON content from text that might contain markdown or other formatting.
        
        Args:
            text: The text to extract JSON from
            
        Returns:
            The extracted JSON string
        """
        # Look for content between triple backticks, common in markdown code blocks
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
        if json_match:
            return json_match.group(1).strip()
        
        # If no code blocks found, return the original text
        return text

