"""
Controller for generating questions using Gemini API
"""
import json
import logging
from google import genai
from typing import List, Optional
from ..models.quiz_question import QuizQuestion
from ..models.prompt_template import PromptTemplate
import os

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
        
    def generate_questions(
        self, 
        count: int,
    ) -> Optional[List[QuizQuestion]]:
        """
        Generate quiz questions using the Gemini API.
        
        Args:
            count: Number of questions to generate
            
        Returns:
            List of QuizQuestion objects or None if an error occurs
        """
        prompt = PromptTemplate.get_prompt_template(count=count)
        logger.debug(f"Prompt for question generation: {prompt[:100]}...")
        try:
            logger.info(f"Sending request to Gemini API for {count} questions")
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
            )
            logger.debug(f"Response from Gemini API received")
            
            # Extract the text content from the response
            if hasattr(response, 'text'):
                response_text = response.text
                logger.debug(f"Retrieved text response from Gemini (first 100 chars): {response_text[:100]}...")
            else:
                response_text = str(response)
                logger.warning(f"Response from Gemini API doesn't have text attribute, using str(response)")
                logger.debug(f"Response stringified (first 100 chars): {response_text[:100]}...")
                
            questions = self._parse_response(response_text)
            logger.info(f"Successfully parsed {len(questions)} questions from the response")
            return questions
        except Exception as e:
            logger.error(f"Error generating questions: {e}", exc_info=True)
            return None
    
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
            logger.debug(f"Extracted JSON from response (first 100 chars): {response_text[:100]}...")
            
            data = json.loads(response_text)
            logger.debug(f"JSON parsed successfully, data type: {type(data)}")
            
            # Handle different possible JSON structures
            if isinstance(data, list):
                # If the response is a list of questions
                logger.debug(f"Response contains a list with {len(data)} items")
                for item in data:
                    question = QuizQuestion.from_dict(item)
                    if question.options:
                        questions.append(question)
                    else:
                        logger.error(f"Question {question} does not have options")
            elif isinstance(data, dict):
                if 'questions' in data:
                    # If the response has a 'questions' key with a list
                    logger.debug(f"Response contains a dictionary with 'questions' key ({len(data.get('questions', []))} items)")
                    for item in data.get('questions', []):
                        question = QuizQuestion.from_dict(item)
                        questions.append(question)
                else:
                    # If the response is a single question
                    logger.debug("Response contains a single question dictionary")
                    question = QuizQuestion.from_dict(data)
                    if question.options:
                        questions.append(question)
                    else:
                        logger.error(f"Question {question} does not have options")
                    
            logger.info(f"Successfully parsed {len(questions)} questions")
            return questions
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            logger.debug(f"Raw response (first 500 chars): {response_text[:500]}...")
            return []
        except KeyError as e:
            logger.error(f"Key error in response data: {e}")
            logger.debug(f"Response data structure causing key error: {response_text[:500]}...")
            return []
        except Exception as e:
            logger.error(f"Unexpected error while parsing response: {e}", exc_info=True)
            logger.debug(f"Raw response causing error (first 500 chars): {response_text[:500]}...")
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
        import re
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
        if json_match:
            logger.debug("Found JSON content in markdown code block")
            return json_match.group(1).strip()
        
        # If no code blocks found, return the original text
        logger.debug("No markdown code blocks found, using original text")
        return text

