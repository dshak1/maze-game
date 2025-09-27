import pygame
import sys
import random
import json

# Initialize Pygame
pygame.init()

# Grid settings
ROWS, COLS = 5, 5
CELL_SIZE = 100
LINE_COLOR = (0, 0, 0)      # Black grid lines
WALL_COLOR = (255, 0, 0)    # Red wall
BG_COLOR = (255, 255, 255)

# Screen setup
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("5x5 Maze - Press 'S' to save, 'L' to load, 'R' to regenerate")

def draw_grid():
    # Draw grid lines
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, HEIGHT), 2)
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, y), (WIDTH, y), 2)



def generate_maze_walls():
    """Generate a maze using recursive backtracking algorithm to ensure all cells are reachable"""
    # Initialize all possible walls as present
    walls = set()
    
    # Add all possible vertical walls
    for row in range(ROWS):
        for col in range(COLS - 1):
            walls.add((row, col, 'v'))
    
    # Add all possible horizontal walls
    for row in range(ROWS - 1):
        for col in range(COLS):
            walls.add((row, col, 'h'))
    
    # Track visited cells
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
    
    def get_neighbors(row, col):
        """Get unvisited neighboring cells"""
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < ROWS and 0 <= new_col < COLS and 
                not visited[new_row][new_col]):
                neighbors.append((new_row, new_col))
        return neighbors
    
    def remove_wall_between(r1, c1, r2, c2):
        """Remove the wall between two adjacent cells"""
        if r1 == r2:  # Same row - vertical wall
            left_col = min(c1, c2)
            walls.discard((r1, left_col, 'v'))
        else:  # Same column - horizontal wall
            top_row = min(r1, r2)
            walls.discard((top_row, c1, 'h'))
    
    # Recursive backtracking maze generation
    def carve_maze(row, col):
        visited[row][col] = True
        neighbors = get_neighbors(row, col)
        random.shuffle(neighbors)
        
        for next_row, next_col in neighbors:
            if not visited[next_row][next_col]:
                remove_wall_between(row, col, next_row, next_col)
                carve_maze(next_row, next_col)
    
    # Start maze generation from top-left corner
    carve_maze(0, 0)
    
    return list(walls)

def draw_walls(walls):
    for wall in walls:
        r, c, typ = wall
        x = c * CELL_SIZE
        y = r * CELL_SIZE
        if typ == 'v':
            pygame.draw.line(screen, WALL_COLOR, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 6)
        else:
            pygame.draw.line(screen, WALL_COLOR, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 6)

def save_walls(walls, filename="maze_walls.json"):
    with open(filename, "w") as f:
        json.dump(walls, f)

def load_walls(filename="maze_walls.json"):
    try:
        with open(filename, "r") as f:
            walls = json.load(f)
        return [tuple(w) for w in walls]
    except Exception:
        return None

# Main loop

# Maze wall state
walls = None

# Try to load walls from file, else generate new maze
walls = load_walls()
if walls is None:
    walls = generate_maze_walls()

while True:
    screen.fill(BG_COLOR)
    draw_grid()
    draw_walls(walls)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_walls(walls)
            elif event.key == pygame.K_l:
                loaded = load_walls()
                if loaded:
                    walls = loaded
            elif event.key == pygame.K_r:
                walls = generate_maze_walls()  # Generate new maze

    pygame.display.flip()