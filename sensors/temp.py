"""
Module to read sensor data from Sense HAT on Raspberry Pi.
"""
from sense_hat import SenseHat

# Initialize Sense HAT for sensor reading
sense = SenseHat()

def get_temperature():
    """
    Return temperature in Celsius from Sense HAT, or None if unavailable.
    
    Returns:
        float or None: Temperature in Celsius
    """
    try:
        return sense.get_temperature()
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

def get_humidity():
    """
    Return humidity percentage from Sense HAT, or None if unavailable.
    
    Returns:
        float or None: Humidity percentage (0-100%)
    """
    try:
        return sense.get_humidity()
    except Exception as e:
        print(f"Error reading humidity: {e}")
        return None

def get_pressure():
    """
    Return pressure in millibars from Sense HAT, or None if unavailable.
    
    Returns:
        float or None: Pressure in millibars
    """
    try:
        return sense.get_pressure()
    except Exception as e:
        print(f"Error reading pressure: {e}")
        return None

def get_all_sensor_data():
    """
    Get all sensor data at once.
    
    Returns:
        dict: Dictionary containing temperature, humidity, and pressure
    """
    return {
        'temperature': get_temperature(),
        'humidity': get_humidity(),
        'pressure': get_pressure()
    }

def get_temperature_from_humidity():
    """
    Return temperature from humidity sensor in Celsius.
    This can be more accurate in some conditions.
    
    Returns:
        float or None: Temperature in Celsius
    """
    try:
        return sense.get_temperature_from_humidity()
    except Exception as e:
        print(f"Error reading temperature from humidity sensor: {e}")
        return None

def get_temperature_from_pressure():
    """
    Return temperature from pressure sensor in Celsius.
    This can be more accurate in some conditions.
    
    Returns:
        float or None: Temperature in Celsius
    """
    try:
        return sense.get_temperature_from_pressure()
    except Exception as e:
        print(f"Error reading temperature from pressure sensor: {e}")
        return None