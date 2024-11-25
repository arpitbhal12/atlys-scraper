import sqlite3
from typing import List, Dict

from db_storage.db_storage_strategy import DBStorageStrategy


class SQLiteStorage(DBStorageStrategy):
    def __init__(self, db_path: str = "products.db"):
        super().__init__()
        self.db_path = db_path

    def save(self, products: List[Dict]) -> None:
        # Insert products into the database
        pass
