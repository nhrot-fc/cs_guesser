"""
Reference class for academic citations
"""
from dataclasses import dataclass
from typing import Optional
from .enums import ReferenceType

@dataclass
class Reference:
    """Academic reference information"""
    type: ReferenceType
    citation: str
    pages: Optional[str] = None
    url: Optional[str] = None
    
    def __str__(self):
        result = f"{self.citation}"
        if self.pages:
            result += f", pp. {self.pages}"
        return result