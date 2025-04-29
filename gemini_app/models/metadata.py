"""
Metadata class for quiz questions
"""
from dataclasses import dataclass, field
from typing import List

@dataclass
class QuestionMetadata:
    """Metadata information for quiz questions"""
    topic: str
    subtopic: str
    difficulty: int
    tags: List[str] = field(default_factory=list)
    
    def __str__(self):
        return f"{self.topic} > {self.subtopic} (Level: {self.difficulty}/5)"