"""
FastAPI application to serve Sense HAT sensor data on Raspberry Pi.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import sqlite3
from datetime import datetime

# Import sensor reading functions
from sensors.temp import get_temperature, get_humidity, get_pressure, get_all_sensor_data

# Import LED display functions
from sensors.led_display import (
    update_led_display, 
    clear_display, 
    show_startup_pattern,
    show_temperature_demo,
    display_sensor_values_text
)

app = FastAPI()

# --- 履歴保存用SQLiteセットアップ ---
DB_PATH = os.path.join(os.path.dirname(__file__), "sensors.db")
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            ts   TEXT PRIMARY KEY,
            temp REAL,
            hum  REAL,
            pres REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Configure template directory relative to this file
templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "web/templates")
)

# Show startup pattern on LED
show_startup_pattern()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Render the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/sensors")
def read_sensors():
    """Return temperature, humidity, and pressure as JSON and update LED display based on all sensor values."""
    temp = get_temperature()
    humidity = get_humidity()
    pressure = get_pressure()

    # --- 履歴に保存 ---
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO history (ts, temp, hum, pres) VALUES (?,?,?,?)",
            (datetime.utcnow().isoformat(), temp, humidity, pressure)
        )
        conn.commit()
    finally:
        conn.close()

    # --- LED表示を更新（温度、湿度、気圧すべてを使用） ---
    update_led_display(temperature=temp, humidity=humidity, pressure=pressure)

    return {
        "temperature": temp,
        "humidity": humidity,
        "pressure": pressure
    }

@app.get("/history")
def read_history(limit: int = 50):
    """
    Return last `limit` sensor records as JSON list of {ts, temperature, humidity, pressure}.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT ts, temp, hum, pres FROM history ORDER BY ts DESC LIMIT ?",
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    rows.reverse()
    return [
        {"ts": ts, "temperature": temp, "humidity": hum, "pressure": pres}
        for ts, temp, hum, pres in rows
    ]

@app.get("/led/clear")
def clear_led():
    """Clear the LED display."""
    clear_display()
    return {"status": "LED display cleared"}

@app.get("/led/startup")
def show_startup():
    """Show startup pattern on LED display."""
    show_startup_pattern()
    return {"status": "Startup pattern displayed"}

@app.get("/led/update")
def manual_led_update():
    """Manually update LED display with current sensor values."""
    temp = get_temperature()
    humidity = get_humidity()
    pressure = get_pressure()
    
    update_led_display(temperature=temp, humidity=humidity, pressure=pressure)
    
    return {
        "status": "LED display updated",
        "temperature": temp,
        "humidity": humidity,
        "pressure": pressure
    }

@app.get("/led/demo")
def show_temperature_color_demo():
    """Show temperature color demonstration on LED display."""
    show_temperature_demo()
    return {"status": "Temperature color demo displayed"}

@app.get("/led/text")
def show_sensor_text():
    """Display current sensor values as scrolling text on LED."""
    temp = get_temperature()
    humidity = get_humidity()
    pressure = get_pressure()
    
    display_sensor_values_text(temp, humidity, pressure)
    
    return {
        "status": "Sensor values displayed as text",
        "temperature": temp,
        "humidity": humidity,
        "pressure": pressure
    }

@app.get("/sensors/all")
def read_all_sensors():
    """Return all sensor data in one call."""
    sensor_data = get_all_sensor_data()
    
    # Update LED display
    update_led_display(
        temperature=sensor_data['temperature'],
        humidity=sensor_data['humidity'],
        pressure=sensor_data['pressure']
    )
    
    return sensor_data