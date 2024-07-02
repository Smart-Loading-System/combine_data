import board
import neopixel
import time
import os
import Edge
import RPi.GPIO as GPIO
from datetime import datetime
import socket

HOST = 'raspberrypi.local'
PORT = 65432

time_now = datetime.now()
image_path = time_now + '.jpg'

pixels = neopixel.NeoPixel(board.D18, 8)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 23
ECHO = 22

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
time.sleep(2)

def request_loadcell_value():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"REQUEST")
        data = s.recv(1024)
    return data.decode('utf-8')

def take_photo():
    # 사진 찍기 전에 LED 색상 변경
    pixels.fill((130,130,130))
    pixels.show()

    # 사진 찍기 (libcamera-jpeg 사용)
    os.system("libcamera-jpeg -o " + image_path + " -t 1000")

    # 1초 대기 후 LED 색상 원래대로 변경
    time.sleep(1)
    pixels.fill((0,0,0))
    pixels.show()

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return image_path, timestamp

GPIO.output(TRIG,True)
time.sleep(0.00001)        # 10uS의 펄스 발생을 위한 딜레이
GPIO.output(TRIG, False)
        
while GPIO.input(ECHO)==0:
    start = time.time()     # Echo핀 상승 시간값 저장
            
while GPIO.input(ECHO)==1:
    stop = time.time()      # Echo핀 하강 시간값 저장
            
check_time = stop - start
distance = check_time * 34300 / 2

'''
pixels.fill((130,130,130))
pixels.show()
os.system("libcamera-jpeg -o " + image_path + " -t 1000")
time.sleep(1)
pixels.fill((0,0,0))
pixels.show()
'''

coner_point = Edge.find_coners(image_path)
print(coner_point)
box_height = 42.03*(1 - (distance/46.7)) 
print("Distance : %.1f cm" % distance)
print("Height : %.1f cm" % box_height)


def main():
    while True:
        input("Press Enter to take a photo...")
        filename, timestamp = take_photo()
        loadcell_value = request_loadcell_value()
        print(f'Photo taken: {filename}')
        print(f'Loadcell value at {timestamp}: {loadcell_value}')

if __name__ == "__main__":
    main()
