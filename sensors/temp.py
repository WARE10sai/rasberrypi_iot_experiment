"""
Module to read data from Sense HAT on Raspberry Pi.
"""
from sense_hat import SenseHat

sense = SenseHat()
# Dim the LED brightness for a softer look

def get_temperature():
    """Return temperature in Celsius from Sense HAT, or None if unavailable."""
    try:
        return sense.get_temperature()
    except Exception:
        return None

def get_humidity():
    """Return humidity percentage from Sense HAT, or None if unavailable."""
    try:
        return sense.get_humidity()
    except Exception:
        return None

def get_pressure():
    """Return pressure in millibars from Sense HAT, or None if unavailable."""
    try:
        return sense.get_pressure()
    except Exception:
        return None