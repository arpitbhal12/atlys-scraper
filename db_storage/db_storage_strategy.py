from abc import abstractmethod, ABCMeta
from typing import List, Dict

class DBStorageStrategy:
    ___metaclasses__ = ABCMeta

    def __init__(self, db_path: str = "products.db"):
        pass

    @abstractmethod
    def save(self, products: List[Dict]) -> None:
        raise NotImplementedError
