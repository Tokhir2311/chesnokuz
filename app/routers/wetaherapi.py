import httpx
import os
from fastapi import FastAPI, HTTPException, Query, APIRouter
from dotenv import load_dotenv
from app.schemas import WeatherResponse

load_dotenv()

API_KEY = os.getenv("API_KEY") 
router = APIRouter(prefix="/weather", tags=["Additions"])


#API_KEY = os.environ.get("WEATHER_API_KEY") 
#BASE_URL = "https://api.openweathermap.org"

@router.get("/weather/", response_model=WeatherResponse)
async def get_weather( city: str ):
    if not API_KEY:
        raise HTTPException(status_code=503, detail="Weather API key not configured")

    async with httpx.AsyncClient() as client:
        response = await client.get(url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}")

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Could not retrieve weather data")
        
        weather_data = response.json()
   
        return weather_data
