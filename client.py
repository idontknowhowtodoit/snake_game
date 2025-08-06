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

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Shared data structure for game state
all_snake_positions = {}

def network_handler():
    global all_snake_positions
    while True:
        try:
            # Receive all players' data from the server
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            
            # Parse the received data (e.g., "pos1|pos2")
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
snake_pos = (5 * SNAKE_SIZE, 5 * SNAKE_SIZE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Send my snake position to the server
    try:
        client_socket.send(str(snake_pos).encode('utf-8'))
    except:
        running = False
        
    # Simulate snake movement for the next turn
    snake_pos = (snake_pos[0] + SNAKE_SIZE, snake_pos[1])
    time.sleep(0.5)

    # Drawing
    screen.fill(BLACK)
    
    # Draw all snakes from the shared data
    for player, pos in all_snake_positions.items():
        color = RED if player == 'player_1' else BLUE
        pygame.draw.rect(screen, color, (pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))
    
    pygame.display.flip()

# Cleanup
client_socket.close()
pygame.quit()