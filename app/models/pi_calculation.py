import random
from dataclasses import dataclass
from typing import Optional

@dataclass
class PiCalculationRequest:
    simulations: int
    concurrency: int = 1

    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate calculation parameters"""
        if not isinstance(self.simulations, int):
            return False, "Simulations must be an integer"
        
        if not isinstance(self.concurrency, int):
            return False, "Concurrency must be an integer"
            
        if not (100 <= self.simulations <= 100_000_000):
            return False, "Simulations must be between 100 and 100,000,000"
            
        if not (1 <= self.concurrency <= 8):
            return False, "Concurrency must be between 1 and 8"
            
        return True, None

@dataclass
class PiCalculationResult:
    pi: float
    simulations: int
    concurrency: int
    execution_time: float 