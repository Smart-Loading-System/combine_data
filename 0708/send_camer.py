import socket
import time
from picamera import PiCamera
from datetime import datetime
import requests
import camera

# 설정
HOST = 'raspberrypi.local'
PORT = 65432
SERVER_URL = 'http://sunghoiot.ddns.net/upload'  # 서버 URL

def request_loadcell_value():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"REQUEST")
        data = s.recv(1024)
    return data.decode('utf-8')

def send_data(coner_point, box_height, loadcell_value, timestamp):
    data = {'loadcell_value': loadcell_value, 'coner_point': coner_point, 'box_height': box_height, 'timestamp': timestamp}
    response = requests.post(SERVER_URL,  data=data)
    
    return response.status_code, response.text

def main():
    while True:
        input("Press Enter to take a photo...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        coner_point, box_height = camera.take_photo()
        loadcell_value = request_loadcell_value()
        print(f'Coner_point: {coner_point}, Height: {box_height}')
        print(f'Loadcell value at {timestamp}: {loadcell_value}')
        response_code, response_text = send_data(coner_point, box_height, loadcell_value, timestamp)
        print(response_code)
        print(response_text)

if __name__ == "__main__":
    main()
