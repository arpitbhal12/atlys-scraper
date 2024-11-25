from fastapi import FastAPI
from pydantic import BaseModel

from db_storage.implementations.json_storage_strategy import JsonStorageStrategy
from scraper import Scraper
from typing import Optional

app = FastAPI()

class ScraperSettings(BaseModel):
    pages_to_scrape: Optional[int] = 10
    proxy: Optional[str] = None

# Rest Endpoint POST request
@app.post("/json-scrape/")
async def start_scraping(settings: ScraperSettings):
    db_strategy = JsonStorageStrategy()
    proxy = settings.proxy
    pages_to_scrap = settings.pages_to_scrape
    scraper = Scraper(pages_to_scrape=pages_to_scrap, proxy=proxy, db_strategy=db_strategy)
    result = scraper.scrape_data()
    return {"message": f"Scraping completed. {result['scraped_count']} products scraped."}
