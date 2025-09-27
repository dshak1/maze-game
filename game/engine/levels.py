"""
Level system for the maze game - progressive difficulty
"""
from enum import Enum
from typing import Dict, List, Tuple, Optional
import random

class GameLevel(Enum):
    EASY = 1
    INTERMEDIATE = 2  
    ADVANCED = 3

class LevelConfig:
    def __init__(self, level: GameLevel):
        self.level = level
        self.title = ""
        self.description = ""
        self.grid_size = (15, 20)  # rows, cols
        self.fog_enabled = False
        self.randomize_on_reset = False
        self.initial_code = ""
        self.hint_text = ""
        self.max_steps_for_perfect = 0
        self.visualization_available = False
        
    @staticmethod
    def get_config(level: GameLevel) -> 'LevelConfig':
        config = LevelConfig(level)
        
        if level == GameLevel.EASY:
            config.title = "Level 1: Treasure Hunt Basics"
            config.description = "Find the treasure chest! Use simple commands to navigate."
            config.grid_size = (12, 16)
            config.fog_enabled = False
            config.randomize_on_reset = False
            config.initial_code = """# Level 1: Basic treasure hunting
# Goal: Reach the treasure chest using simple commands
# Try these commands:

forward(5)
right()
forward(3)
left() 
forward(7)

# Available commands:
# forward(n) - move n steps forward
# left() - turn left
# right() - turn right
# scan() - check what's ahead
# at_goal() - check if at treasure"""
            config.hint_text = "💡 Tip: Look at the maze and plan your path step by step!"
            config.max_steps_for_perfect = 20
            config.visualization_available = False
            
        elif level == GameLevel.INTERMEDIATE:
            config.title = "Level 2: Pattern Recognition"
            config.description = "Use loops to navigate efficiently! Find patterns in your movement."
            config.grid_size = (15, 20)
            config.fog_enabled = False
            config.randomize_on_reset = False
            config.initial_code = """# Level 2: Pattern-based navigation
# Goal: Use loops to reach the treasure efficiently
# Challenge: Solve in 5 lines or less!

# Example pattern - modify this:
for i in range(3):
    forward(4)
    right()

# Try to find the repeating pattern!
# Can you do it in under 5 lines?"""
            config.hint_text = "💡 Tip: Look for repeating movements - right-forward, right-forward..."
            config.max_steps_for_perfect = 25
            config.visualization_available = False
            
        elif level == GameLevel.ADVANCED:
            config.title = "Level 3: A* Search Challenge"
            config.description = "Navigate through fog using smart pathfinding algorithms!"
            config.grid_size = (15, 20)
            config.fog_enabled = True
            config.randomize_on_reset = True
            config.initial_code = """# Level 3: A* Algorithm Challenge
# Goal: Navigate through fog to find treasure
# The maze is randomized each time!

# Smart exploration algorithm:
visited = set()
path = []

while not at_goal() and len(path) < 100:
    current_pos = get_position()
    
    if current_pos not in visited:
        visited.add(current_pos)
    
    # Try to move toward goal
    if scan() != "WALL":
        forward(1)
        path.append("forward")
    else:
        right()
        path.append("right")

# Can you implement A* search?"""
            config.hint_text = "💡 Tip: Use scan() to explore safely. Press V to see visualization!"
            config.max_steps_for_perfect = 30
            config.visualization_available = True
            
        return config

class LevelManager:
    def __init__(self):
        self.current_level = GameLevel.EASY
        self.unlocked_levels = {GameLevel.EASY}  # Start with level 1 unlocked
        self.level_scores = {}  # Track best scores
        
    def get_current_config(self) -> LevelConfig:
        return LevelConfig.get_config(self.current_level)
    
    def set_level(self, level: GameLevel) -> bool:
        """Set current level if unlocked"""
        if level in self.unlocked_levels:
            self.current_level = level
            return True
        return False
    
    def complete_level(self, steps_taken: int) -> Dict:
        """Mark level as complete and unlock next if applicable"""
        config = self.get_current_config()
        
        # Record score
        current_best = self.level_scores.get(self.current_level, float('inf'))
        self.level_scores[self.current_level] = min(current_best, steps_taken)
        
        # Determine performance
        if steps_taken <= config.max_steps_for_perfect:
            performance = "Perfect"
        elif steps_taken <= config.max_steps_for_perfect * 1.5:
            performance = "Excellent"
        elif steps_taken <= config.max_steps_for_perfect * 2:
            performance = "Good"
        else:
            performance = "Completed"
        
        # Unlock next level
        next_level = None
        if self.current_level == GameLevel.EASY:
            next_level = GameLevel.INTERMEDIATE
            self.unlocked_levels.add(GameLevel.INTERMEDIATE)
        elif self.current_level == GameLevel.INTERMEDIATE:
            next_level = GameLevel.ADVANCED  
            self.unlocked_levels.add(GameLevel.ADVANCED)
        
        return {
            "performance": performance,
            "steps": steps_taken,
            "optimal": config.max_steps_for_perfect,
            "next_level_unlocked": next_level,
            "best_score": self.level_scores[self.current_level]
        }
    
    def get_level_status(self) -> Dict:
        """Get status of all levels"""
        status = {}
        for level in GameLevel:
            is_unlocked = level in self.unlocked_levels
            is_current = level == self.current_level
            best_score = self.level_scores.get(level)
            
            status[level] = {
                "unlocked": is_unlocked,
                "current": is_current,
                "completed": best_score is not None,
                "best_score": best_score,
                "config": LevelConfig.get_config(level)
            }
        
        return status