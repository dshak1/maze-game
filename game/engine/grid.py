"""
Grid system for the maze game - handles tiles, walls, weights, and pathfinding
"""
from enum import Enum
from typing import List, Tuple, Dict, Optional
import random

class TileType(Enum):
    EMPTY = "empty"
    WALL = "wall" 
    WEIGHT = "weight"
    START = "start"
    GOAL = "goal"

class Tile:
    def __init__(self, tile_type: TileType = TileType.EMPTY, cost: int = 1):
        self.type = tile_type
        self.cost = cost
        self.visited = False
        self.distance = float('inf')
        self.parent = None
        
    def reset_pathfinding(self):
        """Reset pathfinding data for new search"""
        self.visited = False
        self.distance = float('inf')
        self.parent = None

class Grid:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.tiles = [[Tile() for _ in range(cols)] for _ in range(rows)]
        self.start_pos = (0, 0)
        self.goal_pos = (rows-1, cols-1)
        
    def is_valid_pos(self, row: int, col: int) -> bool:
        """Check if position is within grid bounds"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def get_tile(self, row: int, col: int) -> Optional[Tile]:
        """Get tile at position, return None if invalid"""
        if self.is_valid_pos(row, col):
            return self.tiles[row][col]
        return None
    
    def set_tile(self, row: int, col: int, tile_type: TileType, cost: int = 1):
        """Set tile type and cost at position"""
        if self.is_valid_pos(row, col):
            self.tiles[row][col] = Tile(tile_type, cost)
    
    def neighbors(self, pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], int]]:
        """
        Get neighbors of a position with their movement costs
        Returns list of ((row, col), cost) tuples
        """
        row, col = pos
        neighbors = []
        
        # 4-directional movement (N, E, S, W)
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_pos(new_row, new_col):
                tile = self.tiles[new_row][new_col]
                if tile.type != TileType.WALL:  # Can't move through walls
                    neighbors.append(((new_row, new_col), tile.cost))
        
        return neighbors
    
    def reset_pathfinding(self):
        """Reset all pathfinding data in the grid"""
        for row in self.tiles:
            for tile in row:
                tile.reset_pathfinding()
    
    def set_start(self, row: int, col: int):
        """Set start position"""
        if self.is_valid_pos(row, col):
            # Clear old start
            old_row, old_col = self.start_pos
            if self.tiles[old_row][old_col].type == TileType.START:
                self.tiles[old_row][old_col].type = TileType.EMPTY
            
            # Set new start
            self.start_pos = (row, col)
            self.tiles[row][col].type = TileType.START
    
    def set_goal(self, row: int, col: int):
        """Set goal position"""
        if self.is_valid_pos(row, col):
            # Clear old goal
            old_row, old_col = self.goal_pos
            if self.tiles[old_row][old_col].type == TileType.GOAL:
                self.tiles[old_row][old_col].type = TileType.EMPTY
            
            # Set new goal
            self.goal_pos = (row, col)
            self.tiles[row][col].type = TileType.GOAL
    
    def create_simple_maze(self):
        """Create a simple maze with walls, empty spaces, start and goal"""
        # Clear the grid - everything starts as empty
        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles[row][col] = Tile(TileType.EMPTY, 1)
        
        # Add border walls
        for row in range(self.rows):
            self.tiles[row][0] = Tile(TileType.WALL)
            self.tiles[row][self.cols-1] = Tile(TileType.WALL)
        for col in range(self.cols):
            self.tiles[0][col] = Tile(TileType.WALL)
            self.tiles[self.rows-1][col] = Tile(TileType.WALL)
        
        # Add some internal walls to make it interesting
        wall_positions = [
            # Vertical walls
            (3, 5), (4, 5), (5, 5), (6, 5), (7, 5),
            (3, 15), (4, 15), (5, 15), (6, 15),
            (10, 8), (11, 8), (12, 8), (13, 8),
            # Horizontal walls  
            (8, 10), (8, 11), (8, 12), (8, 13), (8, 14),
            (12, 18), (12, 19), (12, 20), (12, 21),
            (5, 2), (5, 3), (5, 4),
        ]
        
        for row, col in wall_positions:
            if self.is_valid_pos(row, col) and (row, col) not in [self.start_pos, self.goal_pos]:
                self.tiles[row][col] = Tile(TileType.WALL)
        
        # Ensure start and goal are set correctly
        self.tiles[self.start_pos[0]][self.start_pos[1]] = Tile(TileType.START, 1)
        self.tiles[self.goal_pos[0]][self.goal_pos[1]] = Tile(TileType.GOAL, 1)
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])