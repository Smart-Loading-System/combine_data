import socket
import time
from picamera import PiCamera
from datetime import datetime
import requests

# 설정
HOST = 'raspberrypi.local'
PORT = 65432
SERVER_URL = 'http://sunghoiot.ddns.net/upload'  # 서버 URL

def take_photo():
    with PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)  # 카메라 준비 시간
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'/home/pi/photos/photo_{timestamp}.jpg'
        camera.capture(filename)
        camera.stop_preview()
    return filename, timestamp

def request_loadcell_value():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"REQUEST")
        data = s.recv(1024)
    return data.decode('utf-8')

def send_data(filename, timestamp, loadcell_value):
    with open(filename, 'rb') as f:
        files = {'photo': f}
        data = {'timestamp': timestamp, 'loadcell_value': loadcell_value}
        response = requests.post(SERVER_URL, files=files, data=data)
    return response.status_code, response.text

def main():
    while True:
        input("Press Enter to take a photo...")
        filename, timestamp = take_photo()
        loadcell_value = request_loadcell_value()
        print(f'Photo taken: {filename}')
        print(f'Loadcell value at {timestamp}: {loadcell_value}')

if __name__ == "__main__":
    main()
