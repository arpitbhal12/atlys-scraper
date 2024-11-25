from datetime import time

import requests
from bs4 import BeautifulSoup
import os
import json

from typing import Optional


# Helper class for storage (e.g., saving to JSON)
class DBStorage:
    def __init__(self, db_path="/Users/arpitbhal/PycharmProjects/atlys-scraper/products.json"):
        self.db_path = db_path

    def save(self, products):
        # Load existing data if file exists
        if os.path.exists(self.db_path):
            print("open")
            with open(self.db_path, "r") as file:
                content = file.read().strip()
                existing_data = []
                if content:
                    existing_data = json.loads(content) # Read and remove any extra whitespace

            # If the file is empty, assign an empty dictionary (or list) as a fallback
            if not content:
                data = {}
            print("existing data", existing_data)
        else:
            existing_data = []

        # Add new products to existing data
        existing_data.extend(products)

        # Save to the file
        with open(self.db_path, "w") as file:
            json.dump(existing_data, file, indent=4)


# Scraper class
class Scraper:
    def __init__(self, pages_to_scrape: int, proxy: Optional[str] = None):
        self.pages_to_scrape = pages_to_scrape
        self.proxy = proxy
        self.db = DBStorage()

        # Setup a session for requests with proxy if given
        self.session = requests.Session()
        if self.proxy:
            self.session.proxies = {"http": self.proxy, "https": self.proxy}

    def scrape_data(self):
        base_url = "https://dentalstall.com/shop/page/{page_number}/"
        scraped_count = 0
        retry_delay = 5  # seconds

        for page in range(1, self.pages_to_scrape + 1):
            url = base_url.format(page_number=page)
            print(f"Scraping page {page}...")

            # Retry mechanism for fetching pages
            attempts = 3
            for attempt in range(attempts):
                try:
                    response = self.session.get(url)
                    if response.status_code != 200:
                        print(f"Failed to retrieve page {page}, status code: {response.status_code}")
                        continue

                    # Parse the page HTML with BeautifulSoup
                    soup = BeautifulSoup(response.text, "html.parser")
                    products = self.parse_page(soup)
                    print(products[0])
                    self.db.save(products)  # Save scraped products to DB
                    scraped_count += len(products)
                    break  # Successful scraping, move to the next page

                except Exception as e:
                    print(f"Error scraping page {page} on attempt {attempt + 1}: {e}")
                    if attempt < attempts - 1:
                        time.sleep(retry_delay)
                    else:
                        print(f"Skipping page {page} due to repeated failure.")

        return {"scraped_count": scraped_count}

    def parse_page(self, soup: BeautifulSoup):
        products = []

        # Find all the product cards on the page
        product_cards = soup.find_all("li", class_="product")

        for card in product_cards:
            # Extract the product title
            title_tag = card.find("h2", class_="woo-loop-product__title")
            if title_tag:
                title = title_tag.text.strip()
            else:
                continue  # Skip if no title is found

            # Extract the product price
            price_tag = card.find("span", class_="price")
            if price_tag:
                # Check if it contains an offer price or a single price
                price = price_tag.find("ins") or price_tag.find("span", class_="woocommerce-Price-amount")
                if price:
                    price = price.text.strip().replace("₹", "").replace(",", "")
                    price = float(price)
                else:
                    continue  # Skip if no price is found
            else:
                continue  # Skip if no price is found

            # Extract the image URL (handle lazy loading)
            img_tag = card.find("img", class_="attachment-woocommerce_thumbnail")
            image_url = img_tag["data-lazy-src"] if img_tag else ""
            if not image_url:
                continue  # Skip if no image is found

            # Download the image and save it locally
            image_path = image_url

            # Add the product to the list
            product = {
                "product_title": title,
                "product_price": price,
                "path_to_image": image_path
            }
            products.append(product)

        return products

    def download_image(self, image_url: str, title: str):
        # Ensure the image directory exists
        image_dir = "images"
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        # Download the image and save it locally
        image_response = requests.get(image_url)
        image_filename = f"{title}.jpg".replace(" ", "_")  # Sanitize title for filename
        image_path = os.path.join(image_dir, image_filename)

        with open(image_path, "wb") as img_file:
            img_file.write(image_response.content)

        return image_path


# Main function to start scraping
if __name__ == "__main__":
    scraper = Scraper(pages_to_scrape=5, proxy=None)
    result = scraper.scrape_data()
    print(f"Scraping completed. {result['scraped_count']} products scraped.")
