"""
Option class for quiz questions
"""
from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class Option:
    """Represents an answer option for a question"""
    label: str
    answer: bool
    
    def __str__(self):
        return f"{self.label} ({'✓' if self.answer else '✗'})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)