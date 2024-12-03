import asyncio
from typing import Dict, Any, Optional
import uuid
import time

class QueueManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QueueManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._tasks: Dict[str, Dict[str, Any]] = {}
            self._lock = asyncio.Lock()
            self._initialized = True

    async def enqueue_calculation(self, task_data: Dict[str, Any]) -> str:
        """Enqueue a new calculation task"""
        task_id = str(uuid.uuid4())
        
        async with self._lock:
            self._tasks[task_id] = {
                'data': task_data,
                'status': 'pending',
                'result': None,
                'created_at': time.time()
            }
            print(f"Task {task_id} created. Current tasks: {self._tasks}")  # Debug print
        
        return task_id

    async def get_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the result of a calculation task"""
        async with self._lock:
            print(f"Getting result for task {task_id}. Current tasks: {self._tasks}")  # Debug print
            if task_id not in self._tasks:
                return None
            return self._tasks[task_id]

    async def set_result(self, task_id: str, result: Any) -> None:
        """Set the result for a completed task"""
        async with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id]['result'] = result
                self._tasks[task_id]['status'] = 'completed'
                self._tasks[task_id]['completed_at'] = time.time()
                print(f"Task {task_id} completed. Result: {result}")  # Debug print

    async def cleanup_jobs(self, max_age: int = 3600) -> None:
        """Clean up old jobs (older than max_age seconds)"""
        current_time = time.time()
        async with self._lock:
            to_delete = [
                task_id for task_id, task in self._tasks.items()
                if current_time - task['created_at'] > max_age
            ]
            for task_id in to_delete:
                del self._tasks[task_id] 