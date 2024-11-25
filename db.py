# db.py
import json
import os


class DBStorage:
    def __init__(self, db_file: str = "products.json"):
        self.db_file = db_file

        # Create a new file if it doesn't exist
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w") as f:
                json.dump([], f)

    def save(self, product: dict):
        with open(self.db_file, "r") as f:
            data = json.load(f)

        # Check if product already exists in DB
        if not any(p["product_title"] == product["product_title"] for p in data):
            data.append(product)
            with open(self.db_file, "w") as f:
                json.dump(data, f, indent=4)
