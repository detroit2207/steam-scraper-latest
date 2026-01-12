from fastapi import FastAPI
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = FastAPI()

@app.get("/search")
def search_games(query: str):
    api_key = os.getenv("RAWG_API_KEY")
    if not api_key: 
        return {"error": "API key not found"}

    url = f"https://api.rawg.io/api/games?key={api_key}&search={query}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch data from RAWG API"}

    data = response.json()
    return data

@app.get("/")
def read_root():
    return {"Hello": "Worldtest"}

