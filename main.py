"""
FastAPI application to serve Sense HAT sensor data on Raspberry Pi.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import sqlite3
from datetime import datetime
import colorsys

from sensors.temp import sense, get_temperature, get_humidity, get_pressure

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

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Render the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/sensors")
def read_sensors():
    """Return temperature, humidity, and pressure as JSON and update LED color by temperature."""
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

    # --- モダンなLED制御: 温度に応じたグラデーション (青→緑→赤) ---
    if temp is not None:
        # Normalize temperature between 0°C and 40°C
        t_norm = max(0.0, min(temp, 40.0)) / 40.0
        # Map to hue: 0.66 (blue) → 0.33 (green) → 0.0 (red)
        hue = 0.66 * (1 - t_norm)

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