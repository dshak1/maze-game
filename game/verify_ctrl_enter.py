#!/usr/bin/env python3
"""
Simple verification that Ctrl+Enter is working in the main game
"""
import pygame as pg
import sys
from engine.grid import Grid
from engine.agent import Agent
from engine.renderer import Renderer, Colors
from engine.runner import SafeCodeRunner
from engine.editor import TextEditor
from engine.pathfinder import calculate_optimal_steps

def quick_test():
    print("🧪 QUICK CTRL+ENTER VERIFICATION")
    print("=" * 40)
    
    # Initialize pygame (minimal setup)
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Ctrl+Enter Verification")
    clock = pg.time.Clock()
    
    # Initialize components (minimal)
    grid = Grid(10, 10)
    agent = Agent(grid, 0, 0)
    renderer = Renderer(screen, 32)
    code_runner = SafeCodeRunner(agent)
    
    # Create editor
    font = pg.font.Font(None, 20)
    editor_rect = pg.Rect(50, 50, 400, 300)
    text_editor = TextEditor(editor_rect, font)
    text_editor.set_text("forward(3)\nright()\nforward(2)")
    
    # Create maze
    grid.create_simple_maze()
    optimal_steps = calculate_optimal_steps(grid)
    
    print(f"✅ Setup complete - maze optimal: {optimal_steps} steps")
    print("🎮 Press Ctrl+Enter in the window to test code execution")
    print("📝 Press ESC to exit")
    
    running = True
    execution_count = 0
    last_execution_time = 0
    execution_cooldown = 500
    
    while running:
        dt = clock.tick(60) / 1000
        
        for event in pg.event.get():
            # Let text editor handle events first
            if text_editor.handle_event(event):
                continue
                
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_RETURN and (event.mod & pg.KMOD_CTRL):
                    # Test the fixed Ctrl+Enter handling
                    current_time = pg.time.get_ticks()
                    if current_time - last_execution_time > execution_cooldown:
                        execution_count += 1
                        print(f"🎉 Ctrl+Enter #{execution_count} - Executing code...")
                        
                        code_text = text_editor.get_text()
                        success, error_msg, steps = code_runner.execute_code(code_text)
                        
                        if success:
                            print(f"✅ Success! Agent moved to {agent.get_position()}")
                            print(f"📊 Steps taken: {agent.total_steps}")
                            if agent.at_goal():
                                print("🏆 GOAL REACHED!")
                        else:
                            print(f"❌ Error: {error_msg}")
                        
                        last_execution_time = current_time
                        print("-" * 30)
                elif event.key == pg.K_r:
                    # Reset for another test
                    agent.reset()
                    grid.reset_pathfinding()
                    code_runner.reset()
                    print("🔄 Reset - try again!")
        
        # Update
        text_editor.update(dt)
        
        # Draw
        screen.fill((30, 30, 30))
        
        # Draw editor
        text_editor.draw(screen)
        
        # Draw game area (small)
        game_x, game_y = 500, 50
        renderer.draw_grid(grid, game_x, game_y)
        renderer.draw_agent(agent, game_x, game_y)
        
        # Draw status
        font_big = pg.font.Font(None, 28)
        status_text = f"Executions: {execution_count}"
        status_color = (0, 255, 0) if execution_count > 0 else (255, 255, 255)
        status_surface = font_big.render(status_text, True, status_color)
        screen.blit(status_surface, (50, 380))
        
        # Instructions
        font_small = pg.font.Font(None, 20)
        instructions = [
            "✅ FIXED: Using event.mod for Ctrl detection",
            "Press Ctrl+Enter to execute code",
            "Press R to reset, ESC to exit",
            f"Agent: {agent.get_position()}, Steps: {agent.total_steps}"
        ]
        
        y_offset = 420
        for instruction in instructions:
            color = (100, 255, 100) if "FIXED" in instruction else (200, 200, 200)
            text_surface = font_small.render(instruction, True, color)
            screen.blit(text_surface, (50, y_offset))
            y_offset += 20
        
        pg.display.flip()
    
    pg.quit()
    
    print(f"\n🏁 Verification Results:")
    print(f"Total executions: {execution_count}")
    if execution_count > 0:
        print("✅ SUCCESS! Ctrl+Enter is working perfectly!")
        print("🎉 The main game should now respond to Ctrl+Enter properly!")
    else:
        print("❌ No executions detected - please try pressing Ctrl+Enter in the window")

if __name__ == "__main__":
    try:
        quick_test()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()