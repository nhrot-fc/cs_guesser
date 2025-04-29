"""
Enum classes for the gemini_app
"""
from enum import Enum

class ResponseType(Enum):
    UNIQUE_ANSWER = "unique_answer"
    MULTIPLE_ANSWERS = "multiple_answers"

class QuestionType(Enum):
    CONCEPTUAL = "conceptual"
    PRACTICAL = "practical"
    THEORETICAL = "theoretical"
    PROBLEM_SOLVING = "problem_solving"

class ReferenceType(Enum):
    BOOK = "book"
    PAPER = "paper"
    WEBSITE = "website"
    LECTURE = "lecture"