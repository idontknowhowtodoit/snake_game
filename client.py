import socket
import time

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
print(f"서버에 성공적으로 접속했습니다.")

while True:
    try:
        # 서버로 메시지 전송
        message = "Hello from client!"
        client_socket.send(message.encode('utf-8'))
        
        # 서버로부터 응답 수신
        reply = client_socket.recv(1024).decode('utf-8')
        print(f"서버로부터 받은 메시지: {reply}")
        
        # 메시지를 너무 빠르게 보내지 않도록 잠시 대기
        time.sleep(1)
        
    except ConnectionResetError:
        print("서버와의 연결이 끊어졌습니다.")
        break

client_socket.close()