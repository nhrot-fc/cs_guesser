"""
Reference class for academic citations
"""
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class Reference:
    """Academic reference information"""
    type: Optional[str] = None
    title: Optional[str] = None
    authors: Optional[str] = None
    
    def __str__(self) -> str:
        return f"{self.type}: {self.title} by {self.authors}" if self.title else "No title provided"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)