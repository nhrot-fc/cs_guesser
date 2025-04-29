"""
Enum classes for the gemini_app
"""
from enum import Enum

class JSONSerializableEnum(Enum):
    """Base class for enum that can be JSON serialized"""
    
    def for_json(self):
        """Return value for JSON serialization"""
        return self.value
    
    def __str__(self):
        return self.value

class AnswerType(JSONSerializableEnum):
    UNIQUE_ANSWER = "respuesta_unica"
    MULTIPLE_ANSWERS = "respuesta_multiple"

class QuestionType(JSONSerializableEnum):
    CONCEPTUAL = "conceptual"
    PRACTICAL = "practica"
    THEORETICAL = "teorica"
    PROBLEM_SOLVING = "solucion_de_problemas"