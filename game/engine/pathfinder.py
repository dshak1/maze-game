"""
Simple pathfinding utilities for calculating optimal paths
"""
from collections import deque
from typing import List, Tuple, Optional
from .grid import Grid, TileType

def find_shortest_path(grid: Grid, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Find the shortest path using BFS (breadth-first search)
    Returns list of positions from start to goal, or None if no path exists
    """
    if not grid.is_valid_pos(*start) or not grid.is_valid_pos(*goal):
        return None
    
    # BFS queue: (row, col, path)
    queue = deque([(start[0], start[1], [start])])
    visited = {start}
    
    while queue:
        row, col, path = queue.popleft()
        
        # Check if we reached the goal
        if (row, col) == goal:
            return path
        
        # Explore neighbors
        for (next_row, next_col), cost in grid.neighbors((row, col)):
            if (next_row, next_col) not in visited:
                visited.add((next_row, next_col))
                new_path = path + [(next_row, next_col)]
                queue.append((next_row, next_col, new_path))
    
    return None  # No path found

def calculate_optimal_steps(grid: Grid) -> int:
    """Calculate the minimum number of steps needed to reach the goal"""
    path = find_shortest_path(grid, grid.start_pos, grid.goal_pos)
    if path:
        return len(path) - 1  # Subtract 1 because path includes start position
    return -1  # No path possible

def get_efficiency_rating(actual_steps: int, optimal_steps: int) -> str:
    """Get efficiency rating based on step comparison"""
    if optimal_steps <= 0:
        return "No path"
    
    efficiency = optimal_steps / actual_steps if actual_steps > 0 else 0
    
    if efficiency >= 1.0:
        return "Perfect!"
    elif efficiency >= 0.8:
        return "Excellent"
    elif efficiency >= 0.6:
        return "Good"
    elif efficiency >= 0.4:
        return "Fair"
    else:
        return "Needs work"