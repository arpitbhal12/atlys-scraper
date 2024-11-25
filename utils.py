# utils.py
from typing import Optional

import requests
import time


def retry_request(url: str, retries: int = 3, delay: int = 5, proxy: Optional[str] = None):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy} if proxy else None)
            if response.status_code == 200:
                return response
            else:
                print(f"Failed to fetch {url}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching {url}: {str(e)}")

        attempt += 1
        time.sleep(delay)

    return None


def validate_product(product: dict):
    # Simple validation to ensure product data integrity
    return all(key in product for key in ["product_title", "product_price", "path_to_image"])
