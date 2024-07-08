import socket
import threading
import time
import loadcell

w1, w2, w3, w4, total

# 설정
HOST = '0.0.0.0' #모든 연결을 허락하기 위해 0.0.0.0으로 설정한다
PORT = 65432
current_loadcell_value = 0

def read_loadcell_sensor():
    global w1, w2, w3, w4, total
    while True:
        w1, w2, w3, w4, total = loadcell.getRawBytesAndPrintAll()
        time.sleep(0.1)  # 센서 값 갱신 주기

def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    if request.decode('utf-8') == "REQUEST":
        client_socket.sendall(str(w1 + ', ' + w2 + ', ' + w3 + ', ' + w4 + '\n total: ' + total).encode('utf-8'))
    client_socket.close()

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Server listening on port', PORT)
        while True:
            client_socket, addr = s.accept()
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(client_socket,)
            )
            client_handler.start()

def main():
    sensor_thread = threading.Thread(target=read_loadcell_sensor)
    sensor_thread.start()
    server_thread = threading.Thread(target=server)
    server_thread.start()

if __name__ == "__main__":
    main()
