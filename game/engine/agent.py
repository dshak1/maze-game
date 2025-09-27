"""
Agent System
-----------

Manages the player-controlled entity in the maze, including
movement, direction, collision detection, and state tracking.

Features:
- 4-directional movement (North, East, South, West)
- Movement history tracking
- Collision detection with walls
- Forward scanning
- Goal detection
- Position and direction management

Usage:
    from engine.agent import Agent
    from engine.grid import Grid

    grid = Grid(10, 10)
    agent = Agent(grid, start_row=0, start_col=0)

    # Move the agent
    agent.forward(2)
    agent.right()
    agent.forward(1)

    # Check surroundings
    if agent.scan() == 'WALL':
        agent.left()

    # Check for completion
    if agent.at_goal():
        print('Level complete!')
"""
from enum import Enum
from typing import Tuple, Optional
from .grid import Grid, TileType

class Direction(Enum):
    NORTH = 0
    EAST = 1  
    SOUTH = 2
    WEST = 3

class Agent:
    def __init__(self, grid: Grid, start_row: int = 0, start_col: int = 0):
        self.grid = grid
        self.row = start_row
        self.col = start_col
        self.direction = Direction.EAST
        self.move_history = []  # For replay/animation
        self.total_steps = 0  # Count total movement steps
        
        # Movement deltas for each direction
        self.deltas = {
            Direction.NORTH: (-1, 0),
            Direction.EAST: (0, 1), 
            Direction.SOUTH: (1, 0),
            Direction.WEST: (0, -1)
        }
    
    def get_position(self) -> Tuple[int, int]:
        """Get current position as (row, col)"""
        return (self.row, self.col)
    
    def get_front_position(self) -> Tuple[int, int]:
        """Get position in front of agent"""
        dr, dc = self.deltas[self.direction]
        return (self.row + dr, self.col + dc)
    
    def can_move_forward(self) -> bool:
        """Check if agent can move forward"""
        front_row, front_col = self.get_front_position()
        
        if not self.grid.is_valid_pos(front_row, front_col):
            return False
            
        tile = self.grid.get_tile(front_row, front_col)
        return tile and tile.type != TileType.WALL
    
    def forward(self, steps: int = 1) -> bool:
        """
        Move forward by specified steps
        Returns True if all moves successful, False if blocked
        """
        success = True
        for _ in range(steps):
            if self.can_move_forward():
                dr, dc = self.deltas[self.direction]
                self.row += dr
                self.col += dc
                self.total_steps += 1
                self.move_history.append(('forward', self.get_position()))
            else:
                success = False
                break
        return success
    
    def left(self):
        """Turn left (counter-clockwise)"""
        self.direction = Direction((self.direction.value - 1) % 4)
        self.move_history.append(('left', self.direction))
    
    def right(self):
        """Turn right (clockwise)"""
        self.direction = Direction((self.direction.value + 1) % 4)
        self.move_history.append(('right', self.direction))
    
    def scan(self) -> str:
        """
        Scan what's in front of the agent
        Returns 'WALL', 'EMPTY', 'WEIGHT', 'GOAL', or 'BOUNDARY'
        """
        front_row, front_col = self.get_front_position()
        
        if not self.grid.is_valid_pos(front_row, front_col):
            return 'BOUNDARY'
        
        tile = self.grid.get_tile(front_row, front_col)
        if not tile:
            return 'BOUNDARY'
        
        if tile.type == TileType.WALL:
            return 'WALL'
        elif tile.type == TileType.GOAL:
            return 'GOAL'
        elif tile.type == TileType.WEIGHT:
            return 'WEIGHT'
        else:
            return 'EMPTY'
    
    def at_goal(self) -> bool:
        """Check if agent is at the goal position"""
        return (self.row, self.col) == self.grid.goal_pos
    
    def reset(self):
        """Reset agent to start position"""
        self.row, self.col = self.grid.start_pos
        self.direction = Direction.EAST
        self.move_history.clear()
        self.total_steps = 0
    
    def get_direction_symbol(self) -> str:
        """Get Unicode symbol for current direction"""
        symbols = {
            Direction.NORTH: "↑",
            Direction.EAST: "→", 
            Direction.SOUTH: "↓",
            Direction.WEST: "←"
        }
        return symbols[self.direction]