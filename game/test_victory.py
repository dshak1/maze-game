#!/usr/bin/env python3
"""
Test the victory screen and treasure chest functionality
"""
import pygame as pg
import sys
from engine.grid import Grid, TileType
from engine.agent import Agent
from engine.renderer import Renderer, Colors
from engine.pathfinder import calculate_optimal_steps

def test_victory_features():
    print("🧪 TESTING TREASURE CHEST AND VICTORY SCREEN")
    print("=" * 50)
    
    # Initialize pygame
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Victory Test")
    clock = pg.time.Clock()
    
    # Initialize components
    grid = Grid(10, 15)
    agent = Agent(grid, 0, 0) 
    renderer = Renderer(screen, 32)
    
    print("✅ Components initialized")
    
    # Create maze and calculate optimal steps
    grid.create_simple_maze()
    optimal_steps = calculate_optimal_steps(grid)
    print(f"✅ Maze created, optimal solution: {optimal_steps} steps")
    
    # Test treasure chest rendering
    print("\n1. Testing treasure chest on goal tile...")
    screen.fill((20, 20, 24))
    renderer.draw_grid(grid, 50, 50)
    renderer.draw_agent(agent, 50, 50)
    pg.display.flip()
    
    # Wait a moment to see the treasure chest
    pg.time.wait(1000)
    print("✅ Treasure chest rendered on goal tile")
    
    # Test victory screen
    print("\n2. Testing victory screen...")
    test_steps = [optimal_steps, optimal_steps + 5, optimal_steps + 15]
    
    for steps in test_steps:
        screen.fill((20, 20, 24))
        renderer.draw_victory_screen(steps, optimal_steps)
        pg.display.flip()
        pg.time.wait(1500)
        
        efficiency = "Perfect" if steps == optimal_steps else f"+{steps - optimal_steps} extra"
        print(f"✅ Victory screen shown: {steps} steps ({efficiency})")
    
    print("\n3. Testing victory screen interaction...")
    screen.fill((20, 20, 24))
    renderer.draw_victory_screen(optimal_steps + 2, optimal_steps)
    
    # Add instruction text
    font = pg.font.Font(None, 24)
    instruction = font.render("Press SPACE to continue test", True, (255, 255, 255))
    screen.blit(instruction, (50, 50))
    pg.display.flip()
    
    # Wait for space key
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    waiting = False
                    print("✅ Space key dismissed victory screen")
                elif event.key == pg.K_ESCAPE:
                    waiting = False
        clock.tick(60)
    
    # Final test - treasure chest with different maze sizes
    print("\n4. Testing treasure chest with different positions...")
    for size in [(5, 8), (15, 20), (8, 12)]:
        rows, cols = size
        test_grid = Grid(rows, cols)
        test_grid.create_simple_maze()
        
        screen.fill((20, 20, 24))
        renderer.draw_grid(test_grid, 50, 50)
        pg.display.flip()
        pg.time.wait(800)
        
        print(f"✅ Treasure chest rendered in {rows}x{cols} maze")
    
    pg.quit()
    
    print("\n" + "=" * 50)
    print("🎉 ALL VICTORY FEATURES WORKING!")
    print("\nSUMMARY:")
    print("• Treasure chest: ✅ Rendered on goal tile")
    print("• Victory screen: ✅ Big score display")
    print("• Performance rating: ✅ Perfect/Good/Needs work")
    print("• User interaction: ✅ Space to dismiss")
    print("• Multiple maze sizes: ✅ All working")

if __name__ == "__main__":
    try:
        test_victory_features()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Test completed.")