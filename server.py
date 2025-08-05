import socket

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555

# Create a socket and bind it to the server IP and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

# Listen for incoming connections
server_socket.listen()
print(f"서버가 {SERVER_IP}:{SERVER_PORT}에서 접속을 기다리는 중입니다...")

# Accept a client connection
conn, addr = server_socket.accept()
print(f"{addr}에서 접속했습니다.")

while True:
    try:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            print("클라이언트 연결이 끊어졌습니다.")
            break
        print(f"클라이언트로부터 받은 메시지: {data}")
        
        # 클라이언트에게 메시지 전송
        reply = "Server received your message!"
        conn.sendall(reply.encode('utf-8'))
        
    except ConnectionResetError:
        print("클라이언트 연결이 강제로 끊어졌습니다.")
        break
        
conn.close()
server_socket.close()