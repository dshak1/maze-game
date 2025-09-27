"""
Level 1 - Basics: Command API introduction
Goal: Teach basic movement commands and control flow
"""
from engine.grid import Grid, TileType
from engine.agent import Agent

class Level1:
    def __init__(self):
        self.name = "Level 1: Basic Commands"
        self.description = "Learn to move the agent using forward(), left(), and right()"
        
    def setup_level(self, grid: Grid, agent: Agent):
        """Setup a simple maze for learning basic commands"""
        # Clear grid
        for row in range(grid.rows):
            for col in range(grid.cols):
                grid.tiles[row][col].type = TileType.EMPTY
                grid.tiles[row][col].cost = 1
        
        # Create a simple corridor with one turn
        # Add walls to guide the player
        walls = [
            # Top and bottom borders
            *[(0, col) for col in range(grid.cols)],
            *[(grid.rows-1, col) for col in range(grid.cols)],
            # Left and right borders  
            *[(row, 0) for row in range(grid.rows)],
            *[(row, grid.cols-1) for row in range(grid.rows)],
            # Internal walls to create a path
            *[(row, 5) for row in range(1, 8)],  # Vertical wall
            *[(8, col) for col in range(6, 15)],  # Horizontal wall
        ]
        
        for row, col in walls:
            if grid.is_valid_pos(row, col):
                grid.set_tile(row, col, TileType.WALL)
        
        # Set start and goal
        start_pos = (1, 1)
        goal_pos = (10, 15)
        
        grid.set_start(*start_pos)
        grid.set_goal(*goal_pos)
        agent.row, agent.col = start_pos
    
    def get_starter_code(self) -> str:
        """Get the starter code for this level"""
        return """# Level 1: Basic Movement
# Goal: Reach the 🎯 target!
# 
# Available commands:
# forward(n) - move forward n steps
# left()     - turn left 90 degrees  
# right()    - turn right 90 degrees
# scan()     - check what's ahead ("WALL", "EMPTY", "GOAL", "BOUNDARY")
# at_goal()  - returns True if you've reached the goal

# Try this simple path:
forward(4)
right()
forward(7)
left()
forward(2)

# Challenge: Can you solve it using scan() and loops?
"""
    
    def check_success(self, agent: Agent) -> tuple[bool, str, int]:
        """
        Check if level is completed successfully
        Returns (success, message, stars)
        """
        if not agent.at_goal():
            return False, "Not at goal yet!", 0
        
        # Calculate score based on efficiency
        moves = len(agent.move_history)
        optimal_moves = 13  # Minimum moves needed
        
        if moves <= optimal_moves:
            return True, "Perfect! Optimal solution!", 3
        elif moves <= optimal_moves + 3:
            return True, "Great job! Very efficient!", 2
        else:
            return True, "Good work! Try to be more efficient next time.", 1
    
    def get_hints(self, agent: Agent) -> list[str]:
        """Get contextual hints based on agent state"""
        hints = []
        
        # Check if agent is stuck at walls
        scan_result = agent.scan()
        if scan_result == "WALL":
            hints.append("💡 There's a wall ahead! Try turning left() or right()")
        
        # Check if using scan() 
        moves = [move[0] for move in agent.move_history]
        if 'scan' not in str(moves) and len(moves) > 5:
            hints.append("💡 Try using scan() to check what's ahead before moving")
        
        # Check if going in circles
        positions = [move[1] if move[0] == 'forward' else None for move in agent.move_history]
        recent_positions = [p for p in positions[-6:] if p is not None]
        if len(recent_positions) >= 4 and len(set(recent_positions)) <= 2:
            hints.append("💡 You might be going in circles. Plan your path carefully!")
        
        return hints
