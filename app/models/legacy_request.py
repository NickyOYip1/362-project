from dataclasses import dataclass
from typing import Optional, Literal

@dataclass
class LegacyRequest:
    protocol: str  # 'tcp' or 'udp'
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate legacy request parameters"""
        if not isinstance(self.protocol, str):
            return False, "Protocol must be a string"
            
        if self.protocol.lower() not in ['tcp', 'udp']:
            return False, "Protocol must be either 'tcp' or 'udp'"
            
        return True, None

@dataclass
class LegacyResponse:
    pi: float
    count: int
    execution_time: float
    protocol: str 