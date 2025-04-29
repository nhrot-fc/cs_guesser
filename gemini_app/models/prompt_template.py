"""
PromptTemplate class for building prompts with various components
"""
from dataclasses import dataclass
from typing import Dict, Any, List
import json

@dataclass
class PromptTemplate:
    """Structure for building prompts with various components"""
    base_template: str
    feature_templates: Dict[str, Any]
    json_schema: Dict[str, Any]
    full_example: str
    
    def build_prompt(self, topic: str, subtopic: str, difficulty: int, 
                     include_features: List[str] = None) -> str:
        """
        Build a complete prompt for Gemini
        
        Args:
            topic: Main topic for the quiz question
            subtopic: Subtopic for the quiz question
            difficulty: Difficulty level (1-5)
            include_features: List of feature template names to include
            
        Returns:
            str: Complete formatted prompt
        """
        if include_features is None:
            include_features = ["core", "references"]
            
        # Format base prompt
        prompt = self.base_template.format(
            topic=topic,
            subtopic=subtopic if subtopic else "General",
            difficulty=difficulty
        )
        
        # Add requested features
        for feature in include_features:
            if feature in self.feature_templates and "template" in self.feature_templates[feature]:
                if feature == "core":
                    prompt += "\n\n" + self.feature_templates[feature]["template"].format(
                        context="Genera una pregunta desafiante que pruebe la comprensión profunda del tema."
                    )
                else:
                    prompt += "\n\n" + self.feature_templates[feature]["template"]
        
        # Add JSON schema and example
        prompt += f"\n\nDevuelve la respuesta únicamente en este formato JSON:\n{json.dumps(self.json_schema, indent=2)}\n\nEjemplo:\n{self.full_example}"
        
        return prompt