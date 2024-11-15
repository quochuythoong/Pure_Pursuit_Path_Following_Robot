import requests
import time

# ESP32 server IP address
esp32_ip = "http://192.168.1.12"

def send_params(left, right):
    try:
        response = requests.get(f"{esp32_ip}/?left={left}&right={right}")
        if response.status_code == 200:
            print(f"Sent left={left}, right={right} successfully")
        else:
            print(f"Failed to send left={left}, right={right}, status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# Example usage:
send_params(00, 00)
time.sleep(1)
