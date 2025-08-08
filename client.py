import pygame
import socket
import threading
import time

# Pygame initialization
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multiplayer Snake")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Snake properties
SNAKE_SIZE = 20
FPS = 3

# Fonts
font_style = pygame.font.SysFont(None, 30)

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Shared data for game state
all_snake_bodies = {}
food_pos = (0, 0)
my_id = ""
scores = {}
game_over = False
running = True

def network_handler():
    global all_snake_bodies, food_pos, my_id, scores, game_over, running
    while running:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data == "GAMEOVER":
                game_over = True
                print("Game Over")
                continue
            
            if not data:
                break
            
            parts = data.split('|')
            food_pos_str = parts[0].strip('()')
            food_pos = tuple(map(int, food_pos_str.split(',')))
            
            snakes_data = parts[1:]
            
            all_snake_bodies = {}
            for i, snake_str in enumerate(snakes_data):
                if snake_str:
                    body_segments = snake_str.split('),(')
                    body_list = []
                    for segment in body_segments:
                        segment = segment.strip('()')
                        x, y = map(int, segment.split(','))
                        body_list.append((x, y))
                    all_snake_bodies[f'player_{i+1}'] = body_list
            
        except Exception as e:
            print(f"Error in network thread: {e}")
            break
            
    client_socket.close()

network_thread = threading.Thread(target=network_handler)
network_thread.daemon = True
network_thread.start()

# Game loop
clock = pygame.time.Clock()
dx, dy = SNAKE_SIZE, 0

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_SPACE:
                    # Send restart signal to server
                    try:
                        client_socket.send("RESTART".encode('utf-8'))
                        game_over = False
                        dx, dy = SNAKE_SIZE, 0
                    except:
                        running = False
            else:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -SNAKE_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = SNAKE_SIZE, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -SNAKE_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, SNAKE_SIZE

    if not game_over:
        try:
            client_socket.send(str((dx, dy)).encode('utf-8'))
        except:
            running = False

    # Drawing
    screen.fill(BLACK)

    if not game_over:
        # Draw food
        pygame.draw.rect(screen, GREEN, (food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE))

        # Draw all snakes
        for player, body in all_snake_bodies.items():
            color = RED if player == "player_1" else BLUE
            for segment in body:
                pygame.draw.rect(screen, color, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
    else:
        message_surface = font_style.render("Game Over! Press SPACE to Restart", True, WHITE)
        screen.blit(message_surface, [SCREEN_WIDTH/2 - 180, SCREEN_HEIGHT/2 - 20])
    
    pygame.display.flip()

# Cleanup
client_socket.close()
pygame.quit()