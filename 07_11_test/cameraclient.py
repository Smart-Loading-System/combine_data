import socket
import threading
import camera  # camera 모듈을 가져옵니다

# 서버 정보를 설정합니다.
HOST = '127.0.0.1'  # 서버의 주소 (여기서는 로컬호스트)
PORT = 65439  # 서버의 포트 번호

def receive_messages(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print('\nReceived from server:', data.decode())

# 소켓을 생성합니다.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # 서버에 연결을 시도합니다

    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.start()

    while True:
        # 서버로 메시지를 보냅니다.
        message = input("Enter message to send (type 'exit' to quit): ")

        if message == 'take':
            coner_point, box_height = camera.take_photo()
            # 받은 값을 문자열로 변환하여 서버로 전송합니다
            data_to_send = f"coner_point: {coner_point}, box_height: {box_height}"
            s.sendall(data_to_send.encode())
        elif message == 'exit':
            break
        else:
            s.sendall(message.encode())  # 입력한 메시지를 서버로 전송합니다