# Atlys Scraper

This project provides a **FastAPI-based web scraping tool** to scrape product data (name, price, and image) from the **Dentalstall** website and store it in **JSON** format. It is also extensible to other formats, such as **SQL**.

## Features

- Scrape product information (name, price, and image) from the **Dentalstall** website.
- Store scraped data in different storage formats (e.g., **JSON**, **SQLite**, etc.) via the **Strategy Pattern**.
- Configure **proxy** settings for scraping.
- Retry mechanism for failed requests (3 attempts with a 5-second delay).

## Requirements

- Python 3.7+
- **fastapi**
- **uvicorn**
- **requests**
- **beautifulsoup4**
- **pydantic** (for FastAPI request validation)

## Setup and Run Locally


Clone the project

```
git clone https://link-to-project
```

Go to the project directory

```
cd atlys-scraper
```

Install dependencies

```
pip install -r requirements.txt
```

Start the server

```
uvicorn main:app --reload
```

## API Docs
All the API docs can be found here:
``` 
http://localhost:8000/docs
```

## REST API

Do a post request using this cURL:
```
curl --location 'http://127.0.0.1:8000/json-scrape/?token=your_api_token_here' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
    "pages_to_scrape": 1,
    "proxy": "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
  }'
```

After the successful execution of the API, result will be saved in package.json file and all the saved images can be found under images/ directory.