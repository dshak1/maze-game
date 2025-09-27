"""
Level 4 - Algorithm Challenge
---------------------------

A complex maze that requires combining all previous concepts
and developing an efficient algorithmic solution.
"""
from engine.grid import Grid, TileType
from engine.agent import Agent

class Level4:
    def __init__(self):
        self.name = "Algorithm Master"
        self.description = "Create an efficient maze-solving algorithm"
        self.grid_size = 8  # 8x8 grid
        self.minimum_steps = 20
        
    def setup_level(self, grid: Grid, agent: Agent):
        """Setup a complex maze that requires an algorithmic solution"""
        # Resize grid
        grid.rows = self.grid_size
        grid.cols = self.grid_size
        
        # Clear grid
        for row in range(grid.rows):
            for col in range(grid.cols):
                grid.tiles[row][col].type = TileType.EMPTY
                grid.tiles[row][col].cost = 1
        
        # Create a complex maze pattern
        walls = [
            # Border walls
            *[(0, col) for col in range(grid.cols)],
            *[(grid.rows-1, col) for col in range(grid.cols)],
            *[(row, 0) for row in range(grid.rows)],
            *[(row, grid.cols-1) for row in range(grid.rows)],
            
            # Internal maze structure
            (1, 2), (1, 3), (1, 5), (1, 6),
            (2, 2), (2, 5),
            (3, 2), (3, 3), (3, 5), (3, 6),
            (4, 3), (4, 6),
            (5, 1), (5, 2), (5, 3), (5, 5),
            (6, 5),
        ]
        
        for row, col in walls:
            if grid.is_valid_pos(row, col):
                grid.set_tile(row, col, TileType.WALL)
        
        # Set start and goal
        start_pos = (1, 1)
        goal_pos = (6, 6)
        
        grid.set_start(*start_pos)
        grid.set_goal(*goal_pos)
        agent.row, agent.col = start_pos
    
    def get_starter_code(self) -> str:
        """Get the starter code for this level"""
        return """# Level 4: Algorithm Challenge
# Goal: Create an efficient maze-solving algorithm!
#
# This maze requires a systematic approach.
# Try combining all the concepts you've learned:
# - Wall detection with scan()
# - Efficient movement
# - Smart use of loops
# - Decision making

# Here's a starting point for a wall-following algorithm:
while not at_goal():
    # Try to follow the right wall
    right()  # Look right
    if scan() == "EMPTY":
        # If right is clear, go that way
        forward(1)
    else:
        # If right is blocked, look ahead
        left()  # Look forward again
        if scan() == "EMPTY":
            forward(1)
        else:
            # If forward is blocked too, turn left
            left()

# Challenge: Can you modify this to be more efficient?
# Try creating your own algorithm!
"""
    
    def check_success(self, agent: Agent) -> tuple[bool, str, int]:
        """Check if level is completed successfully"""
        if not agent.at_goal():
            return False, "Keep working on your algorithm!", 0
        
        moves = len(agent.move_history)
        
        if moves <= self.minimum_steps:
            return True, "Outstanding! Your algorithm is highly efficient! ⭐⭐⭐", 3
        elif moves <= self.minimum_steps + 10:
            return True, "Good algorithm! Can you optimize it further? ⭐⭐", 2
        else:
            return True, "Algorithm works but needs optimization! ⭐", 1
    
    def get_hints(self, agent: Agent) -> list[str]:
        """Get contextual hints"""
        hints = []
        
        # If they're not using scan enough
        scans = sum(1 for move in agent.move_history if move[0] == 'scan')
        moves = len(agent.move_history)
        
        if moves > 10 and scans < moves / 4:
            hints.append("💡 Try scanning more frequently to make better decisions!")
        
        # If they're going in circles
        positions = [move[1] for move in agent.move_history if move[0] == 'forward']
        recent_pos = positions[-8:] if len(positions) >= 8 else positions
        if len(recent_pos) == len(set(recent_pos)) * 2:
            hints.append("💡 You're revisiting positions! Try a different strategy!")
        
        return hints