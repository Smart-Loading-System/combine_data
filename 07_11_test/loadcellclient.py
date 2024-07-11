import socket
import threading
import loadcell
import time

# 서버 정보를 설정합니다.
HOST = '127.0.0.1'  # 서버의 주소 (여기서는 로컬호스트)
PORT = 65439  # 서버의 포트 번호
count = 0
errorcount = 0

def read_loadcell_sensor():
    
    #w1, w2, w3, w4, total = loadcell.getRawBytesAndPrintAll()
    #return w1, w2, w3, w4, total
    
    total = loadcell.getRawBytesAndPrintAll()
    return total

def receive_messages(sock):
    
    global count,errorcount
    
    while True:
        data = sock.recv(1024)
        if not data:
            break

        if data.decode() == 'take':
            
            #w1, w2, w3, w4, total = read_loadcell_sensor()
            #message = f'{w1}, {w2}, {w3}, {w4}, {total}'
            #sock.sendall(message.encode())
            
            first = read_loadcell_sensor()
            total = first

            while count > 2:
                
                if errorcount > 3:
                    first = read_loadcell_sensor()
                    errorcount = 0
                
                second = read_loadcell_sensor()
                
                if first > second + 50 and first < second - 50:
                    errorcount += 1
                    count = count
                    
                else:
                    total += second
                    count +=1
            
            total = total/3
            message = f'{total}'
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
