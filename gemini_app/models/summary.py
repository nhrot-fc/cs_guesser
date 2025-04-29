"""
Summary class for quiz question explanations
"""
from dataclasses import dataclass, field
from typing import List
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