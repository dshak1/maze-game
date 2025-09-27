"""
Level 3 - Loops and Efficiency
-----------------------------

A maze that teaches using loops for efficient navigation
and introduces the concept of solving problems systematically.
"""
from engine.grid import Grid, TileType
from engine.agent import Agent

class Level3:
    def __init__(self):
        self.name = "Loop Master"
        self.description = "Learn to use loops for efficient navigation"
        self.grid_size = 6  # 6x6 grid
        self.minimum_steps = 12
        
    def setup_level(self, grid: Grid, agent: Agent):
        """Setup a maze that demonstrates the power of loops"""
        # Resize grid
        grid.rows = self.grid_size
        grid.cols = self.grid_size
        
        # Clear grid
        for row in range(grid.rows):
            for col in range(grid.cols):
                grid.tiles[row][col].type = TileType.EMPTY
                grid.tiles[row][col].cost = 1
        
        # Create a maze with a spiral pattern
        walls = [
            # Border walls
            *[(0, col) for col in range(grid.cols)],
            *[(grid.rows-1, col) for col in range(grid.cols)],
            *[(row, 0) for row in range(grid.rows)],
            *[(row, grid.cols-1) for row in range(grid.rows)],
            
            # Spiral walls
            (1, 4), (2, 4), (3, 4), (4, 4),
            (4, 1), (4, 2), (4, 3),
            (2, 1), (2, 2), (2, 3),
        ]
        
        for row, col in walls:
            if grid.is_valid_pos(row, col):
                grid.set_tile(row, col, TileType.WALL)
        
        # Set start and goal
        start_pos = (1, 1)
        goal_pos = (3, 2)
        
        grid.set_start(*start_pos)
        grid.set_goal(*goal_pos)
        agent.row, agent.col = start_pos
    
    def get_starter_code(self) -> str:
        """Get the starter code for this level"""
        return """# Level 3: Loop Master
# Goal: Navigate the spiral using loops!
#
# Hint: You can use a while loop to keep moving until
# you find a wall or reach the goal.
#
# Example loop structure:
while not at_goal():
    if scan() == "WALL":
        right()
    else:
        forward(1)

# Challenge: Can you solve it in fewer steps?
# Try different patterns of movement!
"""
    
    def check_success(self, agent: Agent) -> tuple[bool, str, int]:
        """Check if level is completed successfully"""
        if not agent.at_goal():
            return False, "Keep trying! Think about using a loop!", 0
        
        moves = len(agent.move_history)
        has_loop = any('while' in str(move) or 'for' in str(move) 
                      for move in agent.move_history)
        
        if moves <= self.minimum_steps and has_loop:
            return True, "Perfect! Excellent use of loops! ⭐⭐⭐", 3
        elif has_loop:
            return True, "Good job using loops! Can you be more efficient? ⭐⭐", 2
        else:
            return True, "Goal reached! Try using loops next time! ⭐", 1
    
    def get_hints(self, agent: Agent) -> list[str]:
        """Get contextual hints"""
        hints = []
        
        # Check if they're using loops
        if len(agent.move_history) > self.minimum_steps * 2:
            hints.append("💡 Your solution seems long. Try using a while loop!")
        
        # If they're repeating the same pattern
        moves = [move[0] for move in agent.move_history[-4:]]
        if len(moves) == 4 and len(set(moves)) <= 2:
            hints.append("💡 You're repeating actions! This is what loops are for!")
        
        return hints