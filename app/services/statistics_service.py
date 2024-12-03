import asyncio
from app.models.statistics import RequestStats
from typing import List, Dict

class StatisticsService:
    def __init__(self):
        self._stats: List[RequestStats] = []
        self._lock = asyncio.Lock()

    async def add_request(self, stats: RequestStats) -> None:
        async with self._lock:
            self._stats.append(stats)

    async def get_statistics(self) -> List[Dict]:
        async with self._lock:
            return [stat.__dict__ for stat in self._stats]

    async def clear_statistics(self) -> None:
        async with self._lock:
            self._stats.clear() 