import json
import os
import sqlite3
from typing import List, Dict

from db_storage.db_storage_strategy import DBStorageStrategy


class JsonStorageStrategy(DBStorageStrategy):
    def __init__(self, db_path: str = "products.json"):
        super().__init__()
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump([], f)

    def save(self, products: List):
        # Load existing data if file exists
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as file:
                content = file.read().strip()
                existing_data = []
                if content:
                    existing_data = json.loads(content)  # Read and remove any extra whitespace

            # If the file is empty, assign an empty dictionary (or list) as a fallback
            if not content:
                data = {}
        else:
            existing_data = []

        # Add new products to existing data
        existing_data.extend(products)

        # Save to the file
        with open(self.db_path, "w") as file:
            json.dump(existing_data, file, indent=4)