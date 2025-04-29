"""
Prompt Controller for generating structured prompts for Gemini API
"""
from typing import Dict, List, Any, Optional
from ..models import PromptTemplate
from ..constants import PROMPT_BUILDER, SYLLABUS

class PromptController:
    """Controller for generating and managing prompts for the Gemini API"""
    
    def __init__(self, prompt_template: PromptTemplate = None):
        """Initialize with an optional custom prompt template"""
        self.prompt_template = prompt_template or PROMPT_BUILDER
        self.syllabus = SYLLABUS
    
    def get_topics(self) -> List[str]:
        """Get a list of all available topics from the syllabus"""
        return list(self.syllabus['core_topics'].keys())
    
    def get_subtopics(self, topic: str) -> List[str]:
        """Get subtopics for a specific main topic"""
        if topic in self.syllabus['core_topics']:
            return self.syllabus['core_topics'][topic]
        return []
    
    def generate_prompt(self, 
                       topic: str, 
                       subtopic: Optional[str] = None, 
                       difficulty: int = 3,
                       include_features: Optional[List[str]] = None) -> str:
        """
        Generate a complete prompt for the Gemini API
        
        Args:
            topic: Main topic for the question (e.g., "Algorithms")
            subtopic: Optional specific subtopic (e.g., "Sorting")
            difficulty: Question difficulty on a scale of 1-5
            include_features: Optional list of feature templates to include
            
        Returns:
            str: Complete formatted prompt ready to send to Gemini API
        """
        # Validate inputs
        if topic not in self.get_topics() and topic != "Random":
            raise ValueError(f"Topic '{topic}' not found in syllabus")
        
        if subtopic and topic != "Random" and subtopic not in self.get_subtopics(topic):
            raise ValueError(f"Subtopic '{subtopic}' not found in topic '{topic}'")
            
        if not 1 <= difficulty <= 5:
            raise ValueError("Difficulty must be between 1 and 5")
        
        # Build the prompt using the template
        return self.prompt_template.build_prompt(
            topic=topic,
            subtopic=subtopic,
            difficulty=difficulty,
            include_features=include_features
        )
    
    def validate_response_format(self, response: Dict[str, Any]) -> bool:
        """
        Validate that a response follows the expected format
        
        Args:
            response: The JSON response from Gemini API
            
        Returns:
            bool: Whether the response is valid according to our schema
        """
        required_fields = ["question", "clues", "type", "options"]
        
        for field in required_fields:
            if field not in response:
                return False
                
        if not isinstance(response.get("options"), list) or len(response.get("options", [])) == 0:
            return False
            
        return True