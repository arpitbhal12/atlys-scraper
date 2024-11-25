# main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from scraper import Scraper
from config import API_TOKEN
from typing import Optional

app = FastAPI()

class ScraperSettings(BaseModel):
    pages_to_scrape: Optional[int] = 10
    proxy: Optional[str] = None

# Dependency to check the token
def verify_token(token: str):
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token

@app.post("/scrape/")
async def start_scraping(settings: ScraperSettings, token: str = Depends(verify_token)):
    scraper = Scraper(settings.pages_to_scrape, settings.proxy)
    result = scraper.scrape_data()
    return {"message": f"Scraping completed. {result['scraped_count']} products scraped."}
