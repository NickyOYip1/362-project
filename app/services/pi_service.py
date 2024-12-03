import asyncio
import random
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List
from app.models.pi_calculation import PiCalculationRequest, PiCalculationResult

class PiCalculationService:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=8)

    async def calculate_pi(self, request: PiCalculationRequest) -> PiCalculationResult:
        start_time = time.time()
        
        # Validate request
        is_valid, error = request.validate()
        if not is_valid:
            raise ValueError(error)

        # Calculate points per task
        points_per_task = request.simulations // request.concurrency
        
        # Create tasks
        loop = asyncio.get_event_loop()
        tasks = []
        for _ in range(request.concurrency):
            task = loop.run_in_executor(
                self.executor, 
                self._run_simulation_sync, 
                points_per_task
            )
            tasks.append(task)
        
        # Run simulations concurrently
        results = await asyncio.gather(*tasks)
        
        # Calculate final pi value
        pi = sum(results) / len(results)
        execution_time = time.time() - start_time
        
        return PiCalculationResult(
            pi=pi,
            simulations=request.simulations,
            concurrency=request.concurrency,
            execution_time=execution_time
        )
    
    def _run_simulation_sync(self, num_points: int) -> float:
        """Run a single Monte Carlo simulation"""
        inside_circle = 0
        
        for _ in range(num_points):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            
            # Check if point is inside circle
            if (x * x + y * y) <= 1:
                inside_circle += 1
        
        # Calculate pi for this simulation
        pi = 4 * inside_circle / num_points
        return pi 