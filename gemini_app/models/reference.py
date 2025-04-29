"""
Reference class for academic citations
"""
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class Reference:
    """Academic reference information"""
    type: str
    citation: str
    pages: Optional[str] = None
    url: Optional[str] = None
    
    def __str__(self):
        result = f"{self.citation}"
        if self.pages:
            result += f", pp. {self.pages}"
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        # Convert enum to string for JSON serialization
        result['type'] = self.type
        return result