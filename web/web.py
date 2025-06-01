from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import colorsys

from sensors.temp import sense, get_temperature, get_humidity, get_pressure
from db import save_reading, get_history

app = FastAPI()

# Configure template directory relative to this file
templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/sensors")
def read_sensors():
    temp = get_temperature()
    humidity = get_humidity()
    pressure = get_pressure()

    save_reading(temp, humidity, pressure)

    if temp is not None:
        t_norm = max(0.0, min(temp, 40.0)) / 40.0
        hue = 0.66 * (1 - t_norm)

    return {"temperature": temp, "humidity": humidity, "pressure": pressure}

@app.get("/history")
def read_history(limit: int = 50):
    return get_history(limit)
