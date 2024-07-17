import socket
import threading
import loadcell
import time

# 서버 정보를 설정합니다.
HOST = '192.168.118.242'  # 서버의 주소 (여기서는 로컬호스트)
PORT = 65439  # 서버의 포트 번호

def read_loadcell_sensor():
#    w1, w2, w3, w4, total = loadcell.getRawBytesAndPrintAll()
#    return w1, w2, w3, w4, total

    total = loadcell.getRawBytesAndPrintAll()
    return total


def receive_messages(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break

        #if data.decode().split(' ')[0] == 'coner_point:':
        if data.decode() == 'take':
            count = 0
            errorcount = 0
            total = 0
            
            while count < 3:
                current_reading = read_loadcell_sensor()
        
                if count == 0:
                    previous_reading = current_reading
                    total += current_reading
                    count += 1
                else:
                    if abs(previous_reading - current_reading) > 50:
                        errorcount += 1
                        if errorcount > 3:
                            previous_reading = current_reading
                            errorcount = 0
                    else:
                        total += current_reading
                        previous_reading = current_reading
                        count += 1
            
            average = total / 3
            message = f'{average}'
            sock.sendall(message.encode())
            count = 0
        
        print('\nReceived from server:', data.decode())

# 소켓을 생성합니다.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # 서버에 연결을 시도합니다

    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.start()

    while True:
        # 서버로 메시지를 보냅니다.
        message = input("Enter message to send (type 'exit' to quit): ")
        if message == 'exit':
            break
        s.sendall(message.encode())  # 입력한 메시지를 서버로 전송합니다
