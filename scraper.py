import time
from typing import Optional

import requests
from bs4 import BeautifulSoup
import os
import json

from db_storage.db_storage_strategy import DBStorageStrategy
from db_storage.implementations.json_storage_strategy import JsonStorageStrategy


class DBStorage:
    def __init__(self, db_path="/Users/your_local_directory/atlys-scraper/products.json"):
        self.db_path = db_path

    def save(self, products):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as file:
                content = file.read().strip()
                existing_data = []
                if content:
                    existing_data = json.loads(content)
        else:
            existing_data = []

        existing_data.extend(products)

        with open(self.db_path, "w") as file:
            json.dump(existing_data, file, indent=4)


# Scraper class
class Scraper:
    def __init__(self, pages_to_scrape: int, db_strategy: 'DBStorageStrategy', proxy: Optional[str] = None):
        self.pages_to_scrape = pages_to_scrape
        self.db_strategy = db_strategy
        self.proxy = proxy
        self.session = requests.Session()
        # if self.proxy:
        #     self.session.proxies = {"http": self.proxy, "https": self.proxy}

    def scrape_data(self):
        base_url = "https://dentalstall.com/shop/page/{page_number}/"
        scraped_count = 0
        retry_delay = 5  # seconds

        for page in range(1, self.pages_to_scrape + 1):
            url = base_url.format(page_number=page)
            print(f"Scraping page {page}...")

            attempts = 3
            for attempt in range(attempts):
                try:
                    response = self.session.get(url)
                    if response.status_code != 200:
                        print(f"Failed to retrieve page {page}, status code: {response.status_code}")
                        continue

                    soup = BeautifulSoup(response.text, "html.parser")
                    products = self.parse_page(soup)
                    self.db_strategy.save(products=products)
                    scraped_count += len(products)
                    break
                except Exception as e:
                    print(f"Exception occurred while scraping page {page} error: {str(e)}")
                    if attempt < attempts - 1:
                        time.sleep(retry_delay)
                    else:
                        print(f"Skipping page {page} due to repeated failure.")

        return {"scraped_count": scraped_count}

    def parse_page(self, soup: BeautifulSoup):
        products = []

        product_cards = soup.find_all("li", class_="product")

        for card in product_cards:
            title_tag = card.find("h2", class_="woo-loop-product__title")
            if title_tag:
                title = title_tag.text.strip()
            else:
                continue

            price_tag = card.find("span", class_="price")
            if price_tag:
                price = price_tag.find("ins") or price_tag.find("span", class_="woocommerce-Price-amount")
                if price:
                    price = price.text.strip().replace("₹", "").replace(",", "")
                    price = float(price)
                else:
                    continue
            else:
                continue

            img_tag = card.find("img", class_="attachment-woocommerce_thumbnail")
            image_url = img_tag["data-lazy-src"] if img_tag else ""
            if not image_url:
                continue

            image_path = self.download_image(image_url, title)

            product = {
                "product_title": title,
                "product_price": price,
                "path_to_image": image_path
            }
            products.append(product)

        return products

    def download_image(self, image_url: str, title: str):
        image_dir = "images"
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        image_response = requests.get(image_url)
        image_filename = f"{title}.jpg".replace(" ", "_")  # Sanitize title for filename
        image_path = os.path.join(image_dir, image_filename)

        with open(image_path, "wb") as img_file:
            img_file.write(image_response.content)

        return image_path


if __name__ == "__main__":
    db_strategy = JsonStorageStrategy()
    pages_to_scrap = 1
    scraper = Scraper(pages_to_scrape=pages_to_scrap, proxy=None, db_strategy=db_strategy)
    result = scraper.scrape_data()
    print(f"Scraping completed. {result['scraped_count']} products scraped.")
