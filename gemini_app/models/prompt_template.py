"""
PromptTemplate class for building prompts with various components
"""
from dataclasses import dataclass, asdict
from gemini_app.constants import (
    SYLLABUS,
    FULL_EXAMPLE,
)
from gemini_app.models.enums import (
    QuestionType,
    AnswerType,
)

from typing import List, Dict, Any, Optional
import random

@dataclass
class QuestionParameters:
    """
    Parameters for generating quiz questions.
    """
    topic: str
    subtopic: str
    difficulty: int
    question_type: QuestionType
    response_type: AnswerType
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        # Convert enums to strings for JSON serialization
        result['question_type'] = self.question_type.value
        result['response_type'] = self.response_type.value
        return result


@dataclass
class PromptTemplate:
    """Structure for building prompts with various components"""
    
    @staticmethod
    def get_prompt_template(count: int = 5, question_params: Optional[List[QuestionParameters]] = None) -> str:
        """
        Returns the base prompt template for generating quiz questions.
        This template is used to create structured prompts for the Gemini API.
        
        Args:
            count: Number of questions to generate
            question_params: Optional list of QuestionParameters. If None, random parameters will be generated
            
        Returns:
            A formatted prompt string for the Gemini API
        """
        
        # Generate random question parameters if none provided
        if question_params is None:
            question_params = PromptTemplate._generate_random_question_params(count)
        
        # Building the prompt
        prompt = f"Genera preguntas de admisión para un posgrado (POSCOMP, GeorgiaTech, Harvard, MIT) de computer science con las siguientes características:\n"
        prompt += f"- Número de preguntas: {count}\n"
        prompt += f"- Cantidad de opciones: {5}\n"
        prompt += f"- Cantidad de respuestas correctas: {1}\n"
        prompt += f"- Cantidad de pistas: {5}\n"
        prompt += f"- Formato de respuesta: JSON\n"
        
        
        # Add question specifications
        for i, params in enumerate(question_params):
            prompt += f"Pregunta {i+1}:\n"
            prompt += f"- Tema: {params.topic}\n"
            prompt += f"- Subtema: {params.subtopic}\n"
            prompt += f"- Dificultad: {params.difficulty} (escala 1-5)\n"
            prompt += f"- Tipo de pregunta: {params.question_type.value}\n"
        
        # Add format instructions
        prompt += (
            "\nCada pregunta debe seguir el siguiente formato JSON:\n"
        )
        prompt += f"{FULL_EXAMPLE}\n\n"
        
        prompt += (
            "Requisitos adicionales:\n"
            "- Las preguntas deben ser claras, concisas y relevantes para el nivel de posgrado\n"
            "- Las opciones incorrectas deben ser plausibles y del mismo nivel de complejidad\n"
            "- Asegúrate de que cada pregunta tenga una explicación detallada en la sección \"summary\"\n"
            "- Incluye al menos 2 referencias relevantes para cada pregunta\n"
            "- El formato JSON debe cumplir estrictamente con el esquema proporcionado\n\n"
            "Responde solamente con el JSON de las preguntas generadas.\n"
        )
        
        return prompt
    
    @staticmethod
    def _generate_random_question_params(count: int) -> List[QuestionParameters]:
        """
        Generate a list of random question parameters
        
        Args:
            count: Number of parameter sets to generate
            
        Returns:
            List of QuestionParameters with random values
        """
        params_list = []
        
        # Extract topics from SYLLABUS structure
        topic_names = list(SYLLABUS.keys())
        
        for _ in range(count):
            # Select random topic from the SYLLABUS
            topic = random.choice(topic_names)
            
            # Get subtopics for the selected topic and choose one randomly
            subtopics = SYLLABUS[topic]
            subtopic = random.choice(subtopics) if subtopics else "General"
            
            # Create the parameters object
            params = QuestionParameters(
                topic=topic,
                subtopic=subtopic,
                difficulty=random.randint(1, 5),
                question_type=random.choice(list(QuestionType)),
                response_type=AnswerType.UNIQUE_ANSWER,
            )
            
            params_list.append(params)
            
        return params_list