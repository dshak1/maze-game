#!/usr/bin/env python3
"""
Demo of the complete treasure chest and victory screen functionality
"""
import pygame as pg
import sys
from engine.grid import Grid, TileType
from engine.agent import Agent
from engine.renderer import Renderer, Colors
from engine.runner import SafeCodeRunner
from engine.pathfinder import calculate_optimal_steps, get_efficiency_rating

def demo_complete_game():
    print("🎮 MAZE GAME DEMO - TREASURE CHEST & VICTORY SCREEN")
    print("=" * 60)
    
    # Initialize pygame
    pg.init()
    screen = pg.display.set_mode((1100, 720))
    pg.display.set_caption("Maze Game Demo - Find the Treasure!")
    clock = pg.time.Clock()
    
    # Initialize components
    grid = Grid(18, 25)
    agent = Agent(grid, 0, 0)
    renderer = Renderer(screen, 32)
    code_runner = SafeCodeRunner(agent)
    
    # Create maze
    grid.create_simple_maze()
    optimal_steps = calculate_optimal_steps(grid)
    
    print(f"✅ Demo initialized")
    print(f"📍 Start: {grid.start_pos}, Goal: {grid.goal_pos}")
    print(f"🎯 Optimal solution: {optimal_steps} steps")
    print(f"💎 Look for the treasure chest at the goal!")
    
    # Demo algorithm - simple pathfinding
    demo_code = """
# Simple treasure hunting algorithm
for step in range(100):  # Safety limit
    if at_goal():
        break
    if scan() == "WALL":
        right()
    else:
        forward(1)
"""
    
    show_victory_screen = False
    execution_output = ""
    game_offset_x = 420
    game_offset_y = 100
    
    print("\n🤖 Running automatic treasure hunt...")
    
    running = True
    frame_count = 0
    demo_executed = False
    
    while running:
        frame_count += 1
        dt = clock.tick(60) / 1000
        
        # Auto-execute demo after 3 seconds
        if not demo_executed and frame_count > 180:  # 3 seconds at 60fps
            print("🚀 Executing treasure hunt algorithm...")
            success, error_msg, steps = code_runner.execute_code(demo_code)
            if success:
                steps_taken = agent.total_steps
                efficiency = get_efficiency_rating(steps_taken, optimal_steps)
                
                if agent.at_goal():
                    show_victory_screen = True
                    extra_steps = steps_taken - optimal_steps
                    print(f"🎉 TREASURE FOUND! {steps_taken} steps (optimal: {optimal_steps})")
                    print(f"⭐ Efficiency: {efficiency}")
                    execution_output = f"🏆 TREASURE FOUND in {steps_taken} steps!"
                else:
                    execution_output = f"❌ Algorithm didn't reach treasure: {steps_taken} steps"
                    print(f"❌ Treasure not found after {steps_taken} steps")
            else:
                execution_output = f"❌ Algorithm error: {error_msg}"
                print(f"❌ Algorithm failed: {error_msg}")
            demo_executed = True
        
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE:
                    if show_victory_screen:
                        show_victory_screen = False
                        print("Victory screen dismissed")
                elif event.key == pg.K_r:
                    # Reset for another demo
                    agent.reset()
                    grid.reset_pathfinding()
                    code_runner.reset()
                    show_victory_screen = False
                    demo_executed = False
                    execution_output = "Demo reset - treasure hunt will restart"
                    print("Demo reset!")
        
        # --- DRAW ---
        screen.fill((20, 20, 24))
        
        # Draw demo info panel
        info_rect = pg.Rect(10, 10, 400, 80)
        pg.draw.rect(screen, Colors.DARK_GRAY, info_rect)
        pg.draw.rect(screen, Colors.GRAY, info_rect, 2)
        
        font = pg.font.Font(None, 20)
        info_lines = [
            "🎮 TREASURE HUNT DEMO",
            f"💎 Find treasure at {grid.goal_pos}",
            f"🎯 Optimal path: {optimal_steps} steps",
            "Press R to reset, ESC to exit"
        ]
        
        y_offset = 20
        for line in info_lines:
            text_surface = font.render(line, True, Colors.TEXT_HIGHLIGHT)
            screen.blit(text_surface, (20, y_offset))
            y_offset += 16
        
        # Draw game area
        renderer.draw_grid(grid, game_offset_x, game_offset_y)
        renderer.draw_agent(agent, game_offset_x, game_offset_y)
        
        # Draw status
        status_rect = pg.Rect(game_offset_x, 20, 400, 60)
        pg.draw.rect(screen, Colors.DARK_GRAY, status_rect)
        pg.draw.rect(screen, Colors.GRAY, status_rect, 2)
        
        status_lines = [
            f"Agent: {agent.get_position()} → {agent.get_direction_symbol()}",
            f"Steps: {agent.total_steps}",
            f"Status: {'🎉 TREASURE FOUND!' if agent.at_goal() else '🔍 Searching...'}"
        ]
        
        y_offset = 30
        for line in status_lines:
            text_surface = font.render(line, True, Colors.TEXT)
            screen.blit(text_surface, (game_offset_x + 10, y_offset))
            y_offset += 16
        
        # Draw execution output
        if execution_output:
            output_surface = renderer.font.render(execution_output, True, Colors.TEXT_HIGHLIGHT)
            screen.blit(output_surface, (20, 100))
        
        # Draw victory screen if treasure found
        if show_victory_screen:
            renderer.draw_victory_screen(agent.total_steps, optimal_steps)
        
        pg.display.flip()
        
        # Auto-exit after victory screen is shown for a while
        if show_victory_screen and frame_count > 600:  # 10 seconds after start
            print("🎊 Demo complete! Treasure found successfully!")
            running = False
    
    pg.quit()
    
    print("\n" + "=" * 60)
    print("🎉 TREASURE HUNT DEMO COMPLETE!")
    print("\nFEATURES DEMONSTRATED:")
    print("• 💎 Treasure chest visual on goal tile")
    print("• 🏆 Big victory screen with score")
    print("• ⭐ Performance rating system")
    print("• 🎮 Complete game experience")
    
    if agent.at_goal():
        print(f"\n🏆 FINAL SCORE: {agent.total_steps} STEPS")
        extra = agent.total_steps - optimal_steps
        if extra == 0:
            print("👑 PERFECT! Optimal solution!")
        elif extra <= 5:
            print(f"⭐ EXCELLENT! Only {extra} extra steps")
        else:
            print(f"✅ GOOD! {extra} extra steps (room for improvement)")

if __name__ == "__main__":
    try:
        demo_complete_game()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Demo completed.")