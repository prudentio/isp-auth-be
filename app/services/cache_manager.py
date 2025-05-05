from typing import List
import hashlib
from datetime import date
from pathlib import Path

class CacheManager:
    def __init__(self):
        self.cache = {}
    
    def _get_today(self) -> str:
        return str(date.today())

    def _generate_cache_key(self, filters: List):
        cache_input = str(filters)
        return hashlib.sha256(cache_input.encode('utf-8')).hexdigest()
        
    def set_cache(self, filters: List, file_path: Path, file_name: str):
        today = self._get_today()
        cache_key = self._generate_cache_key(filters)

        if today not in self.cache:
            self.clear_cache()

        self.cache[today][cache_key] = [file_path, file_name]

    def get_cache(self, filters: List):
        today = self._get_today()
        cache_key = self._generate_cache_key(filters)

        if today not in self.cache:
            return None

        cached_data = self.cache[today].get(cache_key)
        return cached_data

    def clear_cache(self) -> None:
        today = self._get_today()
        self.cache = {today: {}}
