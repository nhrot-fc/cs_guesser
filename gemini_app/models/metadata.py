"""
Metadata class for quiz questions
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any

@dataclass
class QuestionMetadata:
    """Metadata information for quiz questions"""
    topic: str
    subtopic: str
    difficulty: int
    tags: List[str] = field(default_factory=list)
    
    def __str__(self):
        return f"{self.topic} > {self.subtopic} (Level: {self.difficulty}/5)"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)