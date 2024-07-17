import socket
import threading

# 서버 정보를 설정합니다.
HOST = '0.0.0.0'  # 로컬호스트
PORT = 65439      # 사용할 포트 번호

clients = []

def handle_client(conn, addr):
    print(f'Connected by {addr}')
    clients.append(conn)
    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f'Received from {addr}: {message}')
                if message == 'reset':
                    print('reset')
                else:
                    broadcast(data, conn)
    finally:
        print(f'Disconnected by {addr}')
        clients.remove(conn)
        conn.close()

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message)
            except:
                client.close()
                clients.remove(client)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on {HOST}:{PORT}')
    
    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()


"""
이거는 csv파일 지우기 코드
import socket
import threading

# 서버 정보를 설정합니다.
HOST = '0.0.0.0'  # 로컬호스트
PORT = 65439      # 사용할 포트 번호

clients = []
csv_file_path = 'data.csv'  # 지우고자 하는 CSV 파일 경로

def handle_client(conn, addr):
    print(f'Connected by {addr}')
    clients.append(conn)
    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f'Received from {addr}: {message}')
                if message == 'reset':
                    clear_csv_file()
                else:
                    broadcast(data, conn)
    finally:
        print(f'Disconnected by {addr}')
        clients.remove(conn)
        conn.close()

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message)
            except:
                client.close()
                clients.remove(client)

def clear_csv_file():
    with open(csv_file_path, 'w') as file:
        file.truncate()
    print('CSV file has been cleared.')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on {HOST}:{PORT}')
    
    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
"""
