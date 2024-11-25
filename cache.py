# cache.py
class Cache:
    def __init__(self):
        self.cache = {}

    def get(self, key: str):
        return self.cache.get(key)

    def set(self, key: str, value: float):
        self.cache[key] = value
