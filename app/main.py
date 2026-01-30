from fastapi import FastAPI , HTTPException, Query 

from app.routers import posts_router , category_router, user_router, tags_router, prof_router, comment_router


import httpx 
import os


from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = FastAPI(
    title="Chesnokdek achchiq yangiliklar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)

app.include_router(posts_router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(tags_router)
app.include_router(prof_router)
app.include_router(comment_router)




# Get the API key from environment variables
# For OpenWeatherMap, the key is called APPID

#API_KEY = os.environ.get("WEATHER_API_KEY") 
BASE_URL = "https://api.openweathermap.org"

@app.get("/weather/")
async def get_weather(city: str = Query(..., description="Tashkent")):
    if not API_KEY:
        raise HTTPException(status_code=503, detail="Weather API key not configured")

    # Parameters for the API request (e.g., units=metric for Celsius)
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric" 
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Could not retrieve weather data")
        
        weather_data = response.json()
        
        # Extract relevant information
        if weather_data.get("cod") == "404":
             raise HTTPException(status_code=404, detail="City not found")

        current_temperature = weather_data["main"]["temp"]
        weather_description = weather_data["weather"][0]["description"]

        return {
            "city": city,
            "temperature_celsius": current_temperature,
            "description": weather_description
        }
