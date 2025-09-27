"""
Test the simplified maze with step counting and efficiency tracking
"""
import pygame as pg
import sys
from engine.grid import Grid, TileType
from engine.agent import Agent
from engine.pathfinder import calculate_optimal_steps, get_efficiency_rating

def test_simplified_maze():
    print("Testing simplified maze with step counting...")
    
    # Create test components
    grid = Grid(10, 15)
    grid.create_simple_maze()
    grid.set_start(2, 2)
    grid.set_goal(7, 12)
    
    agent = Agent(grid, 2, 2)
    agent.reset()
    
    # Calculate optimal path
    optimal_steps = calculate_optimal_steps(grid)
    print(f"Maze created! Start: {grid.start_pos}, Goal: {grid.goal_pos}")
    print(f"Optimal solution requires: {optimal_steps} steps")
    
    # Test different algorithms
    test_cases = [
        ("Direct path", ["forward(5)", "right()", "forward(10)", "right()", "forward(5)"]),
        ("Smart pathfinding", [
            "for step in range(25):",
            "    if at_goal():",
            "        break",
            "    if scan() == 'WALL':",
            "        right()",
            "    else:",
            "        forward(1)"
        ])
    ]
    
    for test_name, commands in test_cases:
        print(f"\n--- Testing {test_name} ---")
        agent.reset()
        
        # Simulate command execution
        for command in commands:
            print(f"  {command}")
        
        # For this test, let's manually execute a simple path
        if test_name == "Direct path":
            agent.forward(5)  # Try to go forward 5
            agent.right()
            agent.forward(10)  # Try to go right 10
            agent.right() 
            agent.forward(5)   # Try to go forward 5
        
        steps_taken = agent.total_steps
        efficiency = get_efficiency_rating(steps_taken, optimal_steps)
        
        print(f"  Result: {steps_taken} steps taken")
        print(f"  Efficiency: {efficiency}")
        print(f"  At goal: {agent.at_goal()}")
        print(f"  Final position: {agent.get_position()}")
        
        if agent.at_goal():
            extra_steps = steps_taken - optimal_steps
            if extra_steps == 0:
                print("  🏆 PERFECT! Optimal solution!")
            else:
                print(f"  🎉 Success! (+{extra_steps} extra steps)")
        else:
            print("  ❌ Did not reach goal")

if __name__ == "__main__":
    test_simplified_maze()