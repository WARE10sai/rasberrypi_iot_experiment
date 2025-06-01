import os
import sqlite3
from datetime import datetime

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

def save_reading(temp, hum, pres):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO history (ts, temp, hum, pres) VALUES (?,?,?,?)",
        (datetime.utcnow().isoformat(), temp, hum, pres)
    )
    conn.commit()
    conn.close()

def get_history(limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT ts, temp, hum, pres FROM history ORDER BY ts DESC LIMIT ?",
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    rows.reverse()
    return [{"ts": ts, "temperature": temp, "humidity": hum, "pressure": pres}
            for ts, temp, hum, pres in rows]
