# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:30:41 2024

@author: ghdtj
"""

import socket
import threading

# 서버 정보를 설정합니다.
HOST = '127.0.0.1'  # 로컬호스트
PORT = 65439        # 사용할 포트 번호

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
                print(f'Received from {addr}: {data.decode()}')
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
