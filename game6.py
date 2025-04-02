import pygame
import random
from collections import deque
import time

# Pygame initialize kar rahe hain
pygame.init()

# Screen dimensions aur colors define kar rahe hain
width, height = 600, 650  # Neeche extra jagah buttons ke liye
rows, cols = 20, 20
box_size = width // cols
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
button_color = (0, 200, 200)

# BFS algorithm ka use karke raasta dhoondhna
def find_way(start, end):
    queue = deque([(start, [start])])
    visited = set([start])
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path  # Agar end mil gaya toh path return karo
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 1 and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
    return []

# Prim's algorithm ka use karke maze generate karna
def create_maze():
    global maze, path_to_end, player_x, player_y
    maze = [[0] * cols for _ in range(rows)]  # Pehle pura maze blank banao
    walls = []
    x, y = 0, 0
    maze[y][x] = 1  # Shuru ka ek block open kar do
    
    # Walls list me adjacent walls daal rahe hain
    walls.extend([(x + dx, y + dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                  if 0 <= x + dx < cols and 0 <= y + dy < rows and maze[y + dy][x + dx] == 0])
    while walls:
        wx, wy = random.choice(walls)
        neighbors = [(wx + dx, wy + dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                     if 0 <= wx + dx < cols and 0 <= wy + dy < rows and maze[wy + dy][wx + dx] == 1]
        if len(neighbors) == 1:
            maze[wy][wx] = 1  # Wall ko path bana do
            walls.extend([(wx + dx, wy + dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                          if 0 <= wx + dx < cols and 0 <= wy + dy < rows and maze[wy + dy][wx + dx] == 0])
        walls.remove((wx, wy))

    # Start aur end points fix kar rahe hain
    maze[0][0] = 1
    maze[rows - 1][cols - 1] = 1
    player_x, player_y = 0, 0  # Player ka position reset karo
    path_to_end = find_way((0, 0), (cols - 1, rows - 1))

# Initial setup
create_maze()
end_x, end_y = cols - 1, rows - 1
auto_move = False
running = True
slow_move = False

# Buttons define karna
auto_button = pygame.Rect((width // 2 - 100, height - 40, 100, 30))
restart_button = pygame.Rect((width // 2 + 10, height - 40, 100, 30))

# Screen setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Game")

# Main game loop
while running:
    screen.fill(white)
    
    # Maze draw karna
    for y in range(rows):
        for x in range(cols):
            color = white if maze[y][x] == 1 else black
            pygame.draw.rect(screen, color, (x * box_size, y * box_size, box_size, box_size))
    
    # Start aur end points draw karna
    pygame.draw.rect(screen, green, (0, 0, box_size, box_size))  # Start point
    pygame.draw.rect(screen, red, (end_x * box_size, end_y * box_size, box_size, box_size))  # End point
    
    # Buttons draw karna
    pygame.draw.rect(screen, button_color, auto_button)
    pygame.draw.rect(screen, button_color, restart_button)
    font = pygame.font.SysFont(None, 24)
    auto_text = font.render("Auto-Solve", True, black)
    restart_text = font.render("Restart", True, black)
    screen.blit(auto_text, (auto_button.x + 10, auto_button.y + 5))
    screen.blit(restart_text, (restart_button.x + 20, restart_button.y + 5))
    
    # Agar auto-solve active hai toh path draw karo
    if auto_move and path_to_end:
        for (px, py) in path_to_end:
            pygame.draw.rect(screen, blue, (px * box_size, py * box_size, box_size, box_size))

        # Slow movement dikhane ke liye ek-ek step le rahe hain
        if slow_move and path_to_end:
            player_x, player_y = path_to_end.pop(0)
            time.sleep(0.1)  
    
    # Player ko draw karna
    pygame.draw.rect(screen, green, (player_x * box_size, player_y * box_size, box_size, box_size))

    # Agar player end point pe pahunch gaya toh game over message
    if (player_x, player_y) == (end_x, end_y) and auto_move:
        print("Congratulations! You reached the end.")
        auto_move = False

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if auto_button.collidepoint(event.pos):
                auto_move = True
                slow_move = True
            elif restart_button.collidepoint(event.pos):
                create_maze()
                auto_move = False
                slow_move = False
        elif event.type == pygame.KEYDOWN and not auto_move:
            new_x, new_y = player_x, player_y
            if event.key == pygame.K_UP and player_y > 0:
                new_y -= 1
            elif event.key == pygame.K_DOWN and player_y < rows - 1:
                new_y += 1
            elif event.key == pygame.K_LEFT and player_x > 0:
                new_x -= 1
            elif event.key == pygame.K_RIGHT and player_x < cols - 1:
                new_x += 1

            # Sirf path pe hi move karne do
            if maze[new_y][new_x] == 1:
                player_x, player_y = new_x, new_y

    pygame.display.flip()
pygame.quit()
