"""
Option class for quiz questions
"""
from dataclasses import dataclass

@dataclass
class Option:
    """Represents an answer option for a question"""
    label: str
    answer: bool
    
    def __str__(self):
        return f"{self.label} ({'✓' if self.answer else '✗'})"