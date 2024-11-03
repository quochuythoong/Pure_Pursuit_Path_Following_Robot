import requests
import time

# ESP32 server IP address
esp32_ip = "http://192.168.1.184"  

def send_param(value):
    try:
        response = requests.get(f"{esp32_ip}/?param={value}")
        if response.status_code == 200:
            print(f"Sent param={value} successfully")
        else:
            print(f"Failed to send param={value}, status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error:", e)

# while(True):
#     for i in range(0,255):
#         send_param(i)

send_param(0)