"""
QuizQuestion class for complete question structure
"""
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional
from .option import Option
from .reference import Reference
from .metadata import QuestionMetadata
from .enums import ResponseType, ReferenceType

@dataclass
class QuizQuestion:
    """Complete quiz question structure that matches the JSON schema"""
    question: str
    clues: List[str]
    type: str  # One of ResponseType values
    options: List[Option]
    metadata: QuestionMetadata
    summary: Optional[str] = None
    references: List[Reference] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the dataclass to a dictionary for JSON serialization"""
        result = asdict(self)
        # Handle any special conversion needed for JSON output
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QuizQuestion':
        """Create a QuizQuestion instance from a dictionary (JSON response)"""
        # Process metadata
        metadata = QuestionMetadata(
            topic=data.get('metadata', {}).get('topic', 'General'),
            subtopic=data.get('metadata', {}).get('subtopic', 'General'),
            difficulty=data.get('metadata', {}).get('difficulty', 3),
            tags=data.get('metadata', {}).get('tags', [])
        )
        
        # Process options
        options = [Option(label=opt.get('label', ''), answer=opt.get('answer', False)) 
                   for opt in data.get('options', [])]
        
        # Process references
        references = []
        for ref in data.get('references', []):
            ref_type = ReferenceType(ref.get('type', 'book'))
            references.append(Reference(
                type=ref_type,
                citation=ref.get('citation', ''),
                pages=ref.get('pages'),
                url=ref.get('url')
            ))
        
        return cls(
            question=data.get('question', ''),
            clues=data.get('clues', []),
            type=data.get('type', ResponseType.UNIQUE_ANSWER.value),
            options=options,
            metadata=metadata,
            summary=data.get('summary', None),
            references=references
        )
    
    def __str__(self):
        """String representation of the quiz question"""
        result = f"Q: {self.question}\n\nClues:"
        for i, clue in enumerate(self.clues, 1):
            result += f"\n{i}. {clue}"
        
        result += f"\n\nType: {self.type}"
        
        result += "\n\nOptions:"
        for i, opt in enumerate(self.options, 1):
            result += f"\n{i}. {opt}"
        
        if self.summary:
            result += f"\n\nExplanation: {self.summary}"
        
        result += f"\n\nMetadata: {self.metadata}"
        
        return result