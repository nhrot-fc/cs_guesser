"""
Summary class for quiz question explanations
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
from .reference import Reference

@dataclass
class Summary:
    """Explanatory summary with references"""
    summary: str
    references: List[Reference] = field(default_factory=list)
    
    def __str__(self):
        result = f"{self.summary}\n\nReferences:"
        for ref in self.references:
            result += f"\n- {ref}"
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = {'summary': self.summary, 'references': []}
        
        for ref in self.references:
            result['references'].append(ref.to_dict())
        
        return result