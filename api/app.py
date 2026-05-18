from fastapi import FastAPI
from main import get_weather

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Weather Forecast API Running"}

@app.get("/weather/{city}")
def weather(city:str):

    data = get_weather(city)

    return data