import socket
import threading

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555

# Stores all connected clients
connected_clients = []
player_data = {}

def broadcast_data():
    while True:
        try:
            # Combine all player data into a single string
            data_to_send = "|".join([str(pos) for pos in player_data.values()])
            
            for client_conn in connected_clients:
                try:
                    client_conn.send(data_to_send.encode('utf-8'))
                except:
                    client_conn.close()
                    
        except:
            break
            
        time.sleep(0.1) # Broadcast every 100ms

def threaded_client(conn, addr, player_id):
    player_data[player_id] = (0, 0) # Initial position
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    
    while True:
        try:
            # Receive snake position from the client
            data = conn.recv(1024).decode('utf-8')
            if not data:
                print(f"클라이언트 {addr}의 연결이 끊어졌습니다.")
                break
            
            # Update player data
            x, y = map(int, data.strip('()').split(','))
            player_data[player_id] = (x, y)
            
        except:
            print(f"클라이언트 {addr}의 연결이 강제로 끊어졌습니다.")
            break
            
    # Clean up on disconnect
    conn.close()
    connected_clients.remove(conn)
    del player_data[player_id]
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_IP, SERVER_PORT))

print(f"서버가 {SERVER_IP}:{SERVER_PORT}에서 접속을 기다리는 중입니다...")
print("두 개의 터미널에서 client.py를 실행하여 접속해 보세요.")

server_socket.listen()

# Start the broadcast thread
broadcast_thread = threading.Thread(target=broadcast_data)
broadcast_thread.daemon = True
broadcast_thread.start()

player_id_counter = 0
while True:
    try:
        conn, addr = server_socket.accept()
        player_id_counter += 1
        print(f"클라이언트 {addr}가 player_{player_id_counter}로 접속했습니다.")
        connected_clients.append(conn)
        
        thread = threading.Thread(target=threaded_client, args=(conn, addr, f"player_{player_id_counter}"))
        thread.start()
        
    except KeyboardInterrupt:
        print("서버를 종료합니다.")
        break
        
server_socket.close()