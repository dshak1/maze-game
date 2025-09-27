"""
Level 2 - Introduction to Scanning
--------------------------------

A maze that introduces the scan() function and teaches
basic conditional logic.
"""
from engine.grid import Grid, TileType
from engine.agent import Agent

class Level2:
    def __init__(self):
        self.name = "Scanner Training"
        self.description = "Learn to use scan() to detect walls"
        self.grid_size = 5  # 5x5 grid
        self.minimum_steps = 8
        
    def setup_level(self, grid: Grid, agent: Agent):
        """Setup a maze that requires wall detection"""
        # Resize grid
        grid.rows = self.grid_size
        grid.cols = self.grid_size
        
        # Clear grid
        for row in range(grid.rows):
            for col in range(grid.cols):
                grid.tiles[row][col].type = TileType.EMPTY
                grid.tiles[row][col].cost = 1
        
        # Create a maze that requires scanning
        walls = [
            # Border walls
            *[(0, col) for col in range(grid.cols)],
            *[(grid.rows-1, col) for col in range(grid.cols)],
            *[(row, 0) for row in range(grid.rows)],
            *[(row, grid.cols-1) for row in range(grid.rows)],
            
            # Internal walls creating a zig-zag path
            (1, 2), (1, 3),
            (2, 1), (2, 2),
            (3, 3), (3, 2)
        ]
        
        for row, col in walls:
            if grid.is_valid_pos(row, col):
                grid.set_tile(row, col, TileType.WALL)
        
        # Set start and goal
        start_pos = (1, 1)
        goal_pos = (3, 1)
        
        grid.set_start(*start_pos)
        grid.set_goal(*goal_pos)
        agent.row, agent.col = start_pos
    
    def get_starter_code(self) -> str:
        """Get the starter code for this level"""
        return """# Level 2: Wall Detection
# Goal: Navigate through the maze using scan()!
#
# New command:
# scan() - Returns what's in front of you:
#   "WALL"   - There's a wall
#   "EMPTY"  - Clear path
#   "GOAL"   - The target!
#
# Try this pattern:
if scan() == "WALL":
    right()  # Turn right if there's a wall
else:
    forward(1)  # Move forward if clear

# Challenge: Can you write a loop to solve the whole maze?
# Hint: while not at_goal():
"""
    
    def check_success(self, agent: Agent) -> tuple[bool, str, int]:
        """Check if level is completed successfully"""
        if not agent.at_goal():
            return False, "Not at goal yet! Try using scan()!", 0
        
        moves = len(agent.move_history)
        scans = sum(1 for move in agent.move_history if move[0] == 'scan')
        
        if moves <= self.minimum_steps and scans > 0:
            return True, "Perfect! You used scan() efficiently! ⭐⭐⭐", 3
        elif scans > 0:
            return True, "Good job using scan()! Can you find a shorter path? ⭐⭐", 2
        else:
            return True, "Goal reached, but try using scan() next time! ⭐", 1
    
    def get_hints(self, agent: Agent) -> list[str]:
        """Get contextual hints"""
        hints = []
        
        # Check if they're using scan
        if len(agent.move_history) > 3:
            has_scan = any(move[0] == 'scan' for move in agent.move_history)
            if not has_scan:
                hints.append("💡 Try using scan() to check for walls before moving!")
        
        # If they keep hitting walls
        wall_hits = sum(1 for move in agent.move_history if 
                       move[0] == 'forward' and not move[1])
        if wall_hits > 2:
            hints.append("💡 You're hitting walls! Use scan() to check before moving.")
        
        return hints