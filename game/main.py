"""
Main Game - Maze Algorithm Learning Platform
-----------------------------------------

This is the main entry point of the maze game. The game is designed to teach
algorithmic thinking through maze-solving challenges.

Features:
- Split-screen interface with code editor and maze visualization
- Real-time code execution
- Visual feedback for algorithm performance
- Multiple levels with increasing complexity
- Leaderboard system for tracking performance

Controls:
- Ctrl+Enter: Execute code
- Ctrl+R: Reset level
- Space: Manual step forward
- D: Toggle distance display
- V: Toggle visited cells
- N: Generate new maze
- ESC: Exit game

Available Commands in Code:
- forward(n): Move n steps forward
- left(): Turn left 90 degrees
- right(): Turn right 90 degrees
- scan(): Check what's ahead
- at_goal(): Check if at goal position

Dependencies:
- Pygame: For graphics and user interface
- Python standard library
"""
import pygame as pg
import sys
from engine.grid import Grid, TileType
from engine.agent import Agent
from engine.renderer import Renderer, Colors
from engine.runner import SafeCodeRunner
from engine.editor import TextEditor
from engine.pathfinder import calculate_optimal_steps, get_efficiency_rating

# Constants from the plan
W, H = 1100, 720
GRID_W = 25     # cols
GRID_H = 18     # rows  
TILE = 32
EDITOR_W = 420  # left panel

def main():
    try:
        print("Initializing pygame...")
        pg.init()
        screen = pg.display.set_mode((W, H))
        pg.display.set_caption("Maze Game - Algorithm Learning Platform")
        clock = pg.time.Clock()
        print("Pygame initialized successfully!")
    except Exception as e:
        print(f"Error initializing pygame: {e}")
        return
    
    try:
        print("Initializing game components...")
        # Initialize game components
        grid = Grid(GRID_H, GRID_W)
        agent = Agent(grid, 0, 0)
        renderer = Renderer(screen, TILE)
        code_runner = SafeCodeRunner(agent)
        
        # Initialize text editor
        font = pg.font.Font(None, 20)
        editor_rect = pg.Rect(10, 50, EDITOR_W - 20, H - 200)
        text_editor = TextEditor(editor_rect, font)
        
        print("Game components initialized!")
    except Exception as e:
        print(f"Error initializing game components: {e}")
        return
    
    try:
        print("Creating maze...")
        # Create a simple maze focused on pathfinding
        grid.create_simple_maze()
        grid.set_start(2, 2)
        grid.set_goal(GRID_H-3, GRID_W-3)
        agent.reset()
        
        # Calculate optimal solution
        optimal_steps = calculate_optimal_steps(grid)
        print(f"Maze created! Optimal solution: {optimal_steps} steps")
    except Exception as e:
        print(f"Error creating maze: {e}")
        return
    
    # Set initial code in the editor
    initial_code = """# Goal: Reach the red target in the fewest steps!
# Press Ctrl+Enter to run your complete algorithm

# Manual pathfinding - try this first:
forward(5)
right()
forward(10)
right()
forward(8)

# Smart algorithm - try this for efficiency:
# for step in range(50):  # Safety limit
#     if at_goal():
#         break
#     if scan() == "WALL":
#         right()
#     else:
#         forward(1)
"""
    text_editor.set_text(initial_code)
    
    show_distances = False
    show_visited = False
    execution_output = ""
    last_execution_time = 0
    execution_cooldown = 500  # milliseconds to prevent rapid re-execution
    
    # Performance stats
    stats = {
        "Steps Taken": 0,
        "Optimal Steps": optimal_steps,
        "Efficiency": "Ready",
        "Goal Distance": 0
    }
    
    running = True
    frame_count = 0
    print("Starting main game loop... (Press ESC or close window to exit)")
    
    while running:
        frame_count += 1
        dt = clock.tick(60) / 1000  # seconds
        
        # Handle events
        for event in pg.event.get():
            # Let text editor handle events first
            if text_editor.handle_event(event):
                continue  # Event was consumed by editor
                
            if event.type == pg.QUIT:
                print("Quit event received")
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    print("ESC pressed - exiting")
                    running = False
                elif event.key == pg.K_RETURN and pg.key.get_pressed()[pg.K_LCTRL]:
                    # Ctrl+Enter - Run code (with cooldown to prevent rapid execution)
                    current_time = pg.time.get_ticks()
                    if current_time - last_execution_time > execution_cooldown:
                        print("Executing complete code block...")
                        code_text = text_editor.get_text()
                        success, error_msg, steps = code_runner.execute_code(code_text)
                        if success:
                            steps_taken = agent.total_steps
                            efficiency = get_efficiency_rating(steps_taken, optimal_steps)
                            
                            if agent.at_goal():
                                extra_steps = steps_taken - optimal_steps
                                if extra_steps == 0:
                                    execution_output = f"� PERFECT! Optimal solution in {steps_taken} steps!"
                                else:
                                    execution_output = f"🎉 SUCCESS! Goal reached in {steps_taken} steps (optimal: {optimal_steps})"
                            else:
                                execution_output = f"✅ Code executed! Steps taken: {steps_taken}"
                            
                            stats["Steps Taken"] = steps_taken
                            stats["Efficiency"] = efficiency
                            print(f"Complete code block executed! Agent took {steps_taken} steps")
                            print(f"Agent final position: {agent.get_position()}")
                        else:
                            execution_output = f"❌ Error: {error_msg}"
                            stats["Efficiency"] = "Error"
                            print(f"Code execution failed: {error_msg}")
                        last_execution_time = current_time
                    else:
                        print(f"Too soon! Wait {(execution_cooldown - (current_time - last_execution_time))/1000:.1f}s before next execution")
                elif event.key == pg.K_r and pg.key.get_pressed()[pg.K_LCTRL]:
                    # Ctrl+R - Reset level
                    agent.reset()
                    grid.reset_pathfinding()
                    code_runner.reset()
                    execution_output = "Level reset!"
                    stats["Steps Taken"] = 0
                    stats["Efficiency"] = "Ready"
                elif event.key == pg.K_d:
                    # Toggle distance display
                    show_distances = not show_distances
                elif event.key == pg.K_v:
                    # Toggle visited display
                    show_visited = not show_visited
                elif event.key == pg.K_n:
                    # Generate new maze
                    grid.create_simple_maze()
                    agent.reset()
                    grid.reset_pathfinding()
                    optimal_steps = calculate_optimal_steps(grid)
                    stats["Steps Taken"] = 0
                    stats["Optimal Steps"] = optimal_steps
                    stats["Efficiency"] = "Ready"
                    execution_output = f"New maze! Optimal solution: {optimal_steps} steps"
                elif event.key == pg.K_SPACE:
                    # Manual step forward for testing
                    agent.forward(1)
        
        # --- UPDATE ---
        # Update text editor cursor animation
        text_editor.update(dt)
        
        # Update stats
        agent_pos = agent.get_position()
        goal_pos = grid.goal_pos
        goal_distance = abs(agent_pos[0] - goal_pos[0]) + abs(agent_pos[1] - goal_pos[1])
        stats["Goal Distance"] = f"{goal_distance} tiles"
        
        # Update animations, algorithm steps, etc.
        
        # --- DRAW ---
        screen.fill((20, 20, 24))
        
        # Draw editor panel background
        editor_bg_rect = pg.Rect(0, 0, EDITOR_W, H)
        pg.draw.rect(screen, Colors.EDITOR_BG, editor_bg_rect)
        pg.draw.rect(screen, Colors.GRAY, editor_bg_rect, 2)
        
        # Draw title
        title = renderer.font.render("Code Editor", True, Colors.TEXT_HIGHLIGHT)
        screen.blit(title, (10, 10))
        
        # Draw the text editor
        text_editor.draw(screen)
        
        # Draw instructions below editor
        instructions = [
            "Goal: Reach the target in minimal steps!",
            "",
            "Controls:",
            "Ctrl+Enter - Run code",
            "Ctrl+R - Reset level",
            "N - New maze",
            "",
            "Functions:",
            "forward(n) - move n steps",
            "left() - turn left", 
            "right() - turn right",
            "scan() - check ahead",
            "at_goal() - check if at target"
        ]
        
        y_offset = H - 150
        for instruction in instructions:
            if y_offset < H - 10:
                text_surface = renderer.small_font.render(instruction, True, Colors.TEXT)
                screen.blit(text_surface, (10, y_offset))
                y_offset += 16
        
        # Draw game view
        game_offset_x = EDITOR_W + 20
        game_offset_y = 50
        
        # Calculate available space for grid
        available_width = W - game_offset_x - 20
        available_height = H - game_offset_y - 100
        
        # Draw grid and agent
        renderer.draw_grid(grid, game_offset_x, game_offset_y)
        
        # Draw pathfinding overlay if enabled
        if show_visited or show_distances:
            renderer.draw_pathfinding_overlay(grid, game_offset_x, game_offset_y, 
                                           show_distances, show_visited)
        
        renderer.draw_agent(agent, game_offset_x, game_offset_y)
        
        # Draw stats panel
        stats_rect = pg.Rect(game_offset_x, H - 90, 300, 80)
        renderer.draw_stats_panel(stats_rect, stats)
        
        # Draw controls help
        help_text = [
            "Controls: Space=Step, D=Distances, V=Visited, N=New maze",
            "Ctrl+Enter=Run code, Ctrl+R=Reset"
        ]
        
        y_offset = 10
        for text in help_text:
            text_surface = renderer.small_font.render(text, True, Colors.TEXT)
            screen.blit(text_surface, (game_offset_x, y_offset))
            y_offset += 20
        
        # Goal status
        if agent.at_goal():
            goal_text = renderer.font.render("🎉 GOAL reached! Press Ctrl+R to reset", 
                                           True, Colors.TEXT_HIGHLIGHT)
            screen.blit(goal_text, (game_offset_x, game_offset_y - 30))
        
        # Execution output
        if execution_output:
            lines = execution_output.split('\n')
            y_offset = H - 150
            for line in lines:
                if y_offset < H - 10:
                    text_surface = renderer.small_font.render(line, True, Colors.TEXT_HIGHLIGHT)
                    screen.blit(text_surface, (20, y_offset))
                    y_offset += 16
        
        pg.display.flip()
        
        # Debug info every 5 seconds
        if frame_count % 300 == 0:
            print(f"Frame {frame_count}, Agent at {agent.get_position()}")
    
    print("Exiting game loop...")
    pg.quit()
    print("Game closed successfully!")
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Program terminated.")