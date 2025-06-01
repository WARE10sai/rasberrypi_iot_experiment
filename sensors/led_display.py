"""
Module to control the 8x8 LED display on Sense HAT based on sensor data.
"""
from sense_hat import SenseHat
import colorsys

# Initialize Sense HAT for LED control
sense = SenseHat()
sense.low_light = True

def update_led_display(temperature=None, humidity=None, pressure=None):
    """
    Update the 8x8 LED display based on temperature, humidity, and pressure.
    
    Args:
        temperature (float): Temperature in Celsius (0-40°C range for optimal display)
        humidity (float): Humidity percentage (0-100%)
        pressure (float): Pressure in millibars (950-1050 hPa range for optimal display)
    
    Display pattern:
        - Temperature: Changes background color (blue=cold, green=normal, red=hot)
        - Humidity: Changes brightness pattern on corners
        - Pressure: Changes central cross pattern (purple=low, yellow=high)
    """
    try:
        # Initialize 8x8 matrix (64 pixels)
        pixels = [[0, 0, 0] for _ in range(64)]
        
        # --- 温度による背景色の設定 (Temperature background color) ---
        if temperature is not None:
            bg_color = _get_temperature_color(temperature)
        else:
            bg_color = [0, 0, 50]  # Default blue
        
        # Fill background with temperature color
        for i in range(64):
            pixels[i] = bg_color.copy()
        
        # --- 湿度による明度パターン (Humidity brightness pattern) ---
        if humidity is not None:
            _apply_humidity_pattern(pixels, humidity)
        
        # --- 気圧による中央パターン (Pressure central pattern) ---
        if pressure is not None:
            _apply_pressure_pattern(pixels, pressure)
        
        # Set the LED matrix
        sense.set_pixels(pixels)
        
    except Exception as e:
        print(f"Error updating LED display: {e}")
        # Fallback: Clear display
        sense.clear()

def _get_temperature_color(temperature):
    """
    Get background color based on temperature.
    
    Args:
        temperature (float): Temperature in Celsius
        
    Returns:
        list: RGB color values [r, g, b]
    """
    # Normalize temperature (0-40°C)
    temp_norm = max(0.0, min(temperature, 40.0)) / 40.0
    
    # Color mapping: Blue (cold) -> Green (normal) -> Red (hot)
    if temp_norm < 0.5:
        # Blue to Green transition
        hue = 0.66 - (temp_norm * 2 * 0.33)  # 0.66 to 0.33
    else:
        # Green to Red transition
        hue = 0.33 - ((temp_norm - 0.5) * 2 * 0.33)  # 0.33 to 0.0
    
    # Convert HSV to RGB
    r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.5)
    return [int(r * 255), int(g * 255), int(b * 255)]

def _apply_humidity_pattern(pixels, humidity):
    """
    Apply humidity-based brightness pattern to corner pixels.
    
    Args:
        pixels (list): 64-element list of RGB values
        humidity (float): Humidity percentage (0-100%)
    """
    # Normalize humidity (0-100%)
    hum_norm = max(0.0, min(humidity, 100.0)) / 100.0
    
    # Create humidity pattern on corners
    brightness_multiplier = 0.5 + (hum_norm * 0.5)  # 0.5 to 1.0
    
    # Corner positions (top-left, top-right, bottom-left, bottom-right)
    corners = [0, 7, 56, 63]
    
    for corner in corners:
        for color_idx in range(3):  # RGB channels
            pixels[corner][color_idx] = int(pixels[corner][color_idx] * brightness_multiplier)

def _apply_pressure_pattern(pixels, pressure):
    """
    Apply pressure-based pattern to central cross area.
    
    Args:
        pixels (list): 64-element list of RGB values
        pressure (float): Pressure in millibars
    """
    # Normalize pressure (950-1050 hPa)
    pres_norm = max(0.0, min(pressure - 950, 100.0)) / 100.0
    
    # Central cross pattern positions
    center_positions = [
        27, 28, 35, 36,  # 2x2 center square
        19, 20, 21,      # top row of cross
        43, 44, 45,      # bottom row of cross
        26, 34, 29, 37   # left and right arms of cross
    ]
    
    # Pressure color mapping
    if pres_norm < 0.5:
        # Low pressure - Purple tones
        intensity = (0.5 - pres_norm) * 2
        press_color = [int(128 * intensity), 0, int(255 * intensity)]
    else:
        # High pressure - Yellow tones
        intensity = (pres_norm - 0.5) * 2
        press_color = [int(255 * intensity), int(255 * intensity), 0]
    
    # Apply pressure pattern
    for pos in center_positions:
        if pos < 64:
            pixels[pos] = press_color

def clear_display():
    """Clear the LED display."""
    try:
        sense.clear()
    except Exception as e:
        print(f"Error clearing display: {e}")

def show_startup_pattern():
    """Show a rainbow spiral startup pattern on the LED display."""
    try:
        # Rainbow colors
        colors = [
            [255, 0, 0],    # Red
            [255, 127, 0],  # Orange
            [255, 255, 0],  # Yellow
            [0, 255, 0],    # Green
            [0, 0, 255],    # Blue
            [75, 0, 130],   # Indigo
            [148, 0, 211],  # Violet
            [255, 255, 255] # White
        ]
        
        # Spiral pattern from center outward
        spiral_order = [
            28, 29, 36, 37, 35, 27, 20, 21,
            22, 30, 38, 46, 45, 44, 43, 42,
            34, 26, 18, 19, 11, 12, 13, 14,
            15, 23, 31, 39, 47, 55, 54, 53,
            52, 51, 50, 49, 41, 33, 25, 17,
            9, 10, 2, 3, 4, 5, 6, 7,
            16, 24, 32, 40, 48, 56, 57, 58,
            59, 60, 61, 62, 63, 1, 0, 8
        ]
        
        # Initialize pixel matrix
        pixels = [[0, 0, 0] for _ in range(64)]
        
        # Apply spiral rainbow pattern
        for i, pos in enumerate(spiral_order):
            color_idx = i % len(colors)
            pixels[pos] = colors[color_idx]
        
        sense.set_pixels(pixels)
        
    except Exception as e:
        print(f"Error showing startup pattern: {e}")

def show_temperature_demo():
    """Show a demonstration of temperature color transitions."""
    try:
        import time
        
        # Demonstrate temperature range from 0°C to 40°C
        for temp in range(0, 41, 2):
            pixels = [[0, 0, 0] for _ in range(64)]
            temp_color = _get_temperature_color(temp)
            
            # Fill display with temperature color
            for i in range(64):
                pixels[i] = temp_color
            
            sense.set_pixels(pixels)
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Error in temperature demo: {e}")

def display_sensor_values_text(temperature, humidity, pressure):
    """
    Display sensor values as scrolling text on the LED matrix.
    
    Args:
        temperature (float): Temperature in Celsius
        humidity (float): Humidity percentage
        pressure (float): Pressure in millibars
    """
    try:
        message = f"T:{temperature:.1f}C H:{humidity:.1f}% P:{pressure:.0f}hPa"
        sense.show_message(message, scroll_speed=0.1, text_colour=[255, 255, 255])
    except Exception as e:
        print(f"Error displaying text: {e}") 