import socket
import threading
import time
import random

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555

# Stores all connected clients
connected_clients = {}
player_data = {}

# Game properties
SNAKE_SIZE = 20
FPS = 3

# Game state
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
food_pos = (random.randrange(0, SCREEN_WIDTH - SNAKE_SIZE, SNAKE_SIZE),
            random.randrange(0, SCREEN_HEIGHT - SNAKE_SIZE, SNAKE_SIZE))

# Control flags
running = True

def game_loop():
    global food_pos
    while running:
        # Check for food collision and move all snakes
        for player_id, snake in list(player_data.items()):
            head = snake['body'][0]
            
            # Move the snake
            new_head = (head[0] + snake['direction'][0], head[1] + snake['direction'][1])
            snake['body'].insert(0, new_head)
            
            # Collision detection (Walls, Self, Other snakes)
            if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
                new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT or
                new_head in snake['body'][1:] or
                any(new_head in other_snake['body'] for other_id, other_snake in player_data.items() if other_id != player_id)):
                
                print(f"클라이언트 {player_id} 충돌! 게임 종료.")
                del player_data[player_id]
                if player_id in connected_clients:
                    try:
                        connected_clients[player_id].send("GAMEOVER".encode('utf-8'))
                    except:
                        pass
                continue

            # Check for food collision
            if head == food_pos:
                snake['score'] += 1
                food_pos = (random.randrange(0, SCREEN_WIDTH - SNAKE_SIZE, SNAKE_SIZE),
                            random.randrange(0, SCREEN_HEIGHT - SNAKE_SIZE, SNAKE_SIZE))
            else:
                snake['body'].pop()
            
        # Combine all player data and food into a single string
        snakes_data = "|".join([",".join([f"({x},{y})" for x, y in snake['body']]) for snake in player_data.values()])
        data_to_send = f"{food_pos}|{snakes_data}"
        
        # Broadcast the new state to all clients
        for client_id, client_conn in list(connected_clients.items()):
            try:
                client_conn.send(data_to_send.encode('utf-8'))
            except:
                client_conn.close()
                del connected_clients[client_id]
                if client_id in player_data:
                    del player_data[client_id]
                
        time.sleep(1 / FPS)

def threaded_client(conn, addr, player_id):
    player_data[player_id] = {
        'body': [(100 * (len(connected_clients)), 100)],
        'direction': (SNAKE_SIZE, 0),
        'score': 0
    }
    
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    while running:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                print(f"클라이언트 {addr}의 연결이 끊어졌습니다.")
                break
            
            if data == "RESTART":
                # Reset player data for restart
                player_data[player_id] = {
                    'body': [(100 * (len(connected_clients)), 100)],
                    'direction': (SNAKE_SIZE, 0),
                    'score': 0
                }
                continue

            dx, dy = map(int, data.strip('()').split(','))
            player_data[player_id]['direction'] = (dx, dy)
            
        except:
            print(f"클라이언트 {addr}의 연결이 강제로 끊어졌습니다.")
            break
            
    conn.close()
    if player_id in connected_clients:
        del connected_clients[player_id]
    if player_id in player_data:
        del player_data[player_id]
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print(f"서버가 {SERVER_IP}:{SERVER_PORT}에서 접속을 기다리는 중입니다...")
print("두 개의 터미널에서 client.py를 실행하여 접속해 보세요.")

game_loop_thread = threading.Thread(target=game_loop)
game_loop_thread.daemon = True
game_loop_thread.start()

player_id_counter = 0
while running:
    try:
        conn, addr = server_socket.accept()
        player_id_counter += 1
        player_id = f"player_{player_id_counter}"
        print(f"클라이언트 {addr}가 {player_id}로 접속했습니다.")
        connected_clients[player_id] = conn
        
        thread = threading.Thread(target=threaded_client, args=(conn, addr, player_id))
        thread.start()
        
    except KeyboardInterrupt:
        print("서버를 종료합니다.")
        running = False
        
server_socket.close()