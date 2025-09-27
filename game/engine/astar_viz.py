"""
A* Algorithm visualization for educational purposes
"""
import pygame as pg
import heapq
from typing import List, Tuple, Dict, Set, Optional
from .grid import Grid, TileType

class AStarVisualizer:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.open_set: List[Tuple[float, int, int]] = []  # Priority queue
        self.closed_set: Set[Tuple[int, int]] = set()
        self.came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        self.g_score: Dict[Tuple[int, int], float] = {}
        self.f_score: Dict[Tuple[int, int], float] = {}
        self.current_node: Optional[Tuple[int, int]] = None
        self.path: List[Tuple[int, int]] = []
        self.step_count = 0
        self.is_complete = False
        
        # Colors for visualization
        self.colors = {
            'open': (0, 255, 0, 100),      # Green for open set
            'closed': (255, 0, 0, 100),    # Red for closed set  
            'current': (255, 255, 0, 150), # Yellow for current node
            'path': (255, 0, 255, 150),    # Magenta for final path
            'start': (0, 255, 0),          # Bright green for start
            'goal': (255, 0, 0)            # Bright red for goal
        }
    
    def heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Manhattan distance heuristic"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions"""
        row, col = pos
        neighbors = []
        
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
            new_row, new_col = row + dr, col + dc
            
            if (0 <= new_row < self.grid.rows and 
                0 <= new_col < self.grid.cols and
                self.grid.tiles[new_row][new_col].type != TileType.WALL):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def initialize(self, start: Tuple[int, int], goal: Tuple[int, int]):
        """Initialize A* search"""
        self.open_set = [(0, start[0], start[1])]
        self.closed_set.clear()
        self.came_from.clear()
        self.g_score = {start: 0}
        self.f_score = {start: self.heuristic(start, goal)}
        self.current_node = None
        self.path = []
        self.step_count = 0
        self.is_complete = False
        self.start_pos = start
        self.goal_pos = goal
    
    def step(self) -> bool:
        """Execute one step of A* algorithm. Returns True if continuing, False if done"""
        if not self.open_set or self.is_complete:
            return False
        
        # Get node with lowest f_score
        current_f, current_row, current_col = heapq.heappop(self.open_set)
        current = (current_row, current_col)
        self.current_node = current
        self.step_count += 1
        
        # Check if we reached the goal
        if current == self.goal_pos:
            self.reconstruct_path()
            self.is_complete = True
            return False
        
        # Move current to closed set
        self.closed_set.add(current)
        
        # Examine neighbors
        for neighbor in self.get_neighbors(current):
            if neighbor in self.closed_set:
                continue
            
            tentative_g = self.g_score[current] + 1  # All moves cost 1
            
            if neighbor not in self.g_score or tentative_g < self.g_score[neighbor]:
                # This path to neighbor is better
                self.came_from[neighbor] = current
                self.g_score[neighbor] = tentative_g
                self.f_score[neighbor] = tentative_g + self.heuristic(neighbor, self.goal_pos)
                
                # Add to open set if not already there
                if not any(n[1:] == neighbor for n in self.open_set):
                    heapq.heappush(self.open_set, 
                                 (self.f_score[neighbor], neighbor[0], neighbor[1]))
        
        return True
    
    def reconstruct_path(self):
        """Reconstruct the optimal path"""
        self.path = []
        current = self.goal_pos
        
        while current in self.came_from:
            self.path.append(current)
            current = self.came_from[current]
        
        self.path.append(self.start_pos)
        self.path.reverse()
    
    def draw_visualization(self, screen: pg.Surface, offset_x: int, offset_y: int, 
                          tile_size: int):
        """Draw A* visualization overlay"""
        # Draw open set (frontier)
        for _, row, col in self.open_set:
            if (row, col) != self.current_node:
                x = offset_x + col * tile_size
                y = offset_y + row * tile_size
                overlay = pg.Surface((tile_size, tile_size), pg.SRCALPHA)
                overlay.fill(self.colors['open'])
                screen.blit(overlay, (x, y))
        
        # Draw closed set (explored)
        for row, col in self.closed_set:
            if (row, col) != self.current_node:
                x = offset_x + col * tile_size
                y = offset_y + row * tile_size
                overlay = pg.Surface((tile_size, tile_size), pg.SRCALPHA)
                overlay.fill(self.colors['closed'])
                screen.blit(overlay, (x, y))
        
        # Draw current node
        if self.current_node:
            row, col = self.current_node
            x = offset_x + col * tile_size
            y = offset_y + row * tile_size
            overlay = pg.Surface((tile_size, tile_size), pg.SRCALPHA)
            overlay.fill(self.colors['current'])
            screen.blit(overlay, (x, y))
        
        # Draw final path
        if self.path:
            for i in range(len(self.path) - 1):
                row1, col1 = self.path[i]
                row2, col2 = self.path[i + 1]
                
                x1 = offset_x + col1 * tile_size + tile_size // 2
                y1 = offset_y + row1 * tile_size + tile_size // 2
                x2 = offset_x + col2 * tile_size + tile_size // 2
                y2 = offset_y + row2 * tile_size + tile_size // 2
                
                pg.draw.line(screen, self.colors['path'][:3], (x1, y1), (x2, y2), 4)
        
        # Draw info panel
        self.draw_info_panel(screen, offset_x, offset_y - 100, tile_size)
    
    def draw_info_panel(self, screen: pg.Surface, x: int, y: int, tile_size: int):
        """Draw information panel about the algorithm"""
        font = pg.font.Font(None, 20)
        
        info_lines = [
            f"A* Algorithm Visualization - Step {self.step_count}",
            f"Open Set (Green): {len(self.open_set)} nodes",
            f"Closed Set (Red): {len(self.closed_set)} nodes",
            f"Current Node: {self.current_node}" if self.current_node else "Current Node: None",
            f"Path Length: {len(self.path) - 1}" if len(self.path) > 1 else "Path: Not found",
            "Status: " + ("Complete!" if self.is_complete else "Searching...")
        ]
        
        # Background
        panel_height = len(info_lines) * 22 + 10
        panel_rect = pg.Rect(x, y, 400, panel_height)
        pg.draw.rect(screen, (0, 0, 0, 180), panel_rect)
        pg.draw.rect(screen, (100, 100, 100), panel_rect, 2)
        
        # Text
        for i, line in enumerate(info_lines):
            color = (0, 255, 0) if "Complete" in line else (255, 255, 255)
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (x + 10, y + 10 + i * 22))
    
    def get_statistics(self) -> Dict:
        """Get algorithm statistics"""
        return {
            "steps": self.step_count,
            "nodes_explored": len(self.closed_set),
            "nodes_in_frontier": len(self.open_set),
            "path_length": len(self.path) - 1 if len(self.path) > 1 else 0,
            "is_complete": self.is_complete,
            "optimal_path": self.path.copy() if self.path else []
        }