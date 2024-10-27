import requests
import time

# ESP32 server IP address
esp32_ip = "http://192.168.1.184"  

def control_led(state):
    """Send command to ESP32 to turn LED on or off."""
    if state == "ON":
        requests.get(f"{esp32_ip}/LED=ON")
        print("LED turned ON")
    elif state == "OFF":
        requests.get(f"{esp32_ip}/LED=OFF")
        print("LED turned OFF")
    else:
        print("Invalid state")

# Example usage
while True:
    control_led("ON")
    time.sleep(1)
    control_led("OFF")
    time.sleep(1)
