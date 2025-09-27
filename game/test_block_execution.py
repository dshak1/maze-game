"""
Test complete code block execution
"""
import pygame as pg
import sys
from engine.grid import Grid, TileType
from engine.agent import Agent
from engine.runner import SafeCodeRunner

def test_block_execution():
    print("Testing complete code block execution...")
    
    # Set up minimal game components
    grid = Grid(10, 10)
    agent = Agent(grid, 1, 1)
    runner = SafeCodeRunner(agent)
    
    # Create simple maze
    grid.set_start(1, 1)
    grid.set_goal(5, 5)
    agent.reset()
    
    print(f"Starting position: {agent.get_position()}")
    
    # Test code block that should execute as one unit
    test_code = """
# This entire block should execute at once
steps = 0
while not at_goal() and steps < 20:
    steps += 1
    
    if scan() == "WALL":
        right()
    else:
        forward(1)

# Simple completion check
if at_goal():
    result = "SUCCESS"
else:
    result = "INCOMPLETE"
"""
    
    print("\n" + "="*50)
    print("EXECUTING CODE BLOCK:")
    print("="*50)
    
    success, error, steps = runner.execute_code(test_code)
    
    print("="*50)
    print("EXECUTION COMPLETE")
    print("="*50)
    
    if success:
        print(f"✅ Success! {len(steps)} operations executed")
        print(f"Final position: {agent.get_position()}")
        print(f"At goal: {agent.at_goal()}")
    else:
        print(f"❌ Error: {error}")
    
    print("\nExecution steps:")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")

if __name__ == "__main__":
    test_block_execution()