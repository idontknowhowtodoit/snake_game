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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Snake properties
SNAKE_SIZE = 20
FPS = 10

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Shared data structure for game state
all_snake_positions = {}
player_id = ""
my_snake_pos = (5 * SNAKE_SIZE, 5 * SNAKE_SIZE)

def network_handler():
    global all_snake_positions
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            
            positions = data.split('|')
            all_snake_positions = {}
            for i, pos_str in enumerate(positions):
                if pos_str:
                    x, y = map(int, pos_str.strip('()').split(','))
                    all_snake_positions[f'player_{i+1}'] = (x, y)
                    
        except:
            break
            
    client_socket.close()

# Start the network thread
network_thread = threading.Thread(target=network_handler)
network_thread.daemon = True
network_thread.start()

# Game loop
running = True
clock = pygame.time.Clock()
dx, dy = SNAKE_SIZE, 0 # Initial movement direction (Right)

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -SNAKE_SIZE, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = SNAKE_SIZE, 0
            elif event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -SNAKE_SIZE
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, SNAKE_SIZE

    # Update my snake position
    my_snake_pos = (my_snake_pos[0] + dx, my_snake_pos[1] + dy)
    
    # Send my snake position to the server
    try:
        client_socket.send(str(my_snake_pos).encode('utf-8'))
    except:
        running = False
    
    # Drawing
    screen.fill(BLACK)
    
    for player, pos in all_snake_positions.items():
        color = RED if player_id == "" else BLUE
        pygame.draw.rect(screen, color, (pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))
    
    pygame.display.flip()

# Cleanup
client_socket.close()
pygame.quit()