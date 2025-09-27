#!/usr/bin/env python3
"""
Complete demo of the 3-level maze game system
"""
import pygame as pg
import sys
import time
from engine.grid import Grid, TileType
from engine.agent import Agent
from engine.renderer import Renderer, Colors
from engine.runner import SafeCodeRunner
from engine.levels import LevelManager, GameLevel
from engine.fog import FogOfWar, FogRenderer
from engine.astar_viz import AStarVisualizer

def demo_level_progression():
    print("🎮 MAZE GAME LEVEL SYSTEM DEMO")
    print("=" * 60)
    
    # Initialize pygame
    pg.init()
    screen = pg.display.set_mode((1100, 720))
    pg.display.set_caption("Maze Game - Progressive Level Demo")
    clock = pg.time.Clock()
    
    # Initialize level system
    level_manager = LevelManager()
    
    # Demo each level
    levels_to_demo = [GameLevel.EASY, GameLevel.INTERMEDIATE, GameLevel.ADVANCED]
    
    for i, level in enumerate(levels_to_demo):
        print(f"\n{i+1}. DEMONSTRATING {level.name} LEVEL")
        print("-" * 40)
        
        # Force unlock for demo purposes
        level_manager.unlocked_levels.add(level)
        level_manager.set_level(level)
        config = level_manager.get_current_config()
        
        print(f"Level: {config.title}")
        print(f"Description: {config.description}")
        print(f"Grid Size: {config.grid_size}")
        print(f"Fog Enabled: {config.fog_enabled}")
        print(f"Target Steps: {config.max_steps_for_perfect}")
        print(f"Visualization: {config.visualization_available}")
        
        # Initialize components for this level
        grid = Grid(config.grid_size[0], config.grid_size[1])
        grid.create_simple_maze()
        agent = Agent(grid, 0, 0)
        renderer = Renderer(screen, 32)
        
        # Special features for Level 3
        fog = None
        fog_renderer = None
        astar_viz = None
        
        if config.fog_enabled:
            fog = FogOfWar(grid)
            fog_renderer = FogRenderer()
            fog.update_vision(agent.row, agent.col)
            
        if config.visualization_available:
            astar_viz = AStarVisualizer(grid)
            astar_viz.initialize(grid.start_pos, grid.goal_pos)
        
        # Demo this level for 5 seconds
        demo_frames = 300  # 5 seconds at 60fps
        frame_count = 0
        
        print(f"Demonstrating for 5 seconds...")
        
        while frame_count < demo_frames:
            frame_count += 1
            
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        return
                    elif event.key == pg.K_SPACE:
                        # Skip to next level
                        frame_count = demo_frames
            
            # Draw
            screen.fill((20, 20, 24))
            
            # Draw level info panel
            info_rect = pg.Rect(20, 20, 400, 120)
            pg.draw.rect(screen, (40, 40, 60), info_rect)
            pg.draw.rect(screen, Colors.GRAY, info_rect, 2)
            
            font = pg.font.Font(None, 24)
            small_font = pg.font.Font(None, 18)
            
            # Level info
            title_text = font.render(config.title, True, Colors.TEXT_HIGHLIGHT)
            desc_text = small_font.render(config.description, True, Colors.TEXT)
            hint_text = small_font.render(config.hint_text, True, (150, 255, 150))
            
            screen.blit(title_text, (30, 30))
            screen.blit(desc_text, (30, 55))
            screen.blit(hint_text, (30, 75))
            
            # Features text
            features = []
            if config.fog_enabled:
                features.append("🌫️ Fog of War")
            if config.visualization_available:
                features.append("🔍 A* Visualization")
            if not features:
                features.append("👶 Basic Navigation")
                
            feature_text = small_font.render(" • ".join(features), True, (255, 255, 100))
            screen.blit(feature_text, (30, 95))
            
            # Progress bar
            progress = frame_count / demo_frames
            progress_rect = pg.Rect(30, 115, 360, 10)
            pg.draw.rect(screen, (100, 100, 100), progress_rect)
            progress_fill = pg.Rect(30, 115, int(360 * progress), 10)
            pg.draw.rect(screen, (0, 255, 0), progress_fill)
            
            # Draw maze
            game_offset_x = 450
            game_offset_y = 50
            
            renderer.draw_grid(grid, game_offset_x, game_offset_y)
            renderer.draw_agent(agent, game_offset_x, game_offset_y)
            
            # Level-specific rendering
            if level == GameLevel.ADVANCED:
                # Show A* visualization
                if astar_viz and frame_count % 30 == 0:  # Step every 0.5 seconds
                    astar_viz.step()
                if astar_viz:
                    astar_viz.draw_visualization(screen, game_offset_x, game_offset_y, 32)
                
                # Show fog of war
                if fog and fog_renderer:
                    fog_renderer.draw_fog_overlay(screen, grid, fog, game_offset_x, game_offset_y, 32)
            
            # Instructions
            instruction_text = small_font.render("Press SPACE to skip to next level, ESC to exit", True, Colors.TEXT)
            screen.blit(instruction_text, (20, 680))
            
            pg.display.flip()
            clock.tick(60)
        
        print(f"✅ {config.title} demo completed")
    
    # Final summary screen
    print("\n🎊 DEMO COMPLETE!")
    screen.fill((20, 20, 24))
    
    font = pg.font.Font(None, 48)
    medium_font = pg.font.Font(None, 32)
    small_font = pg.font.Font(None, 24)
    
    # Title
    title = font.render("🏆 MAZE GAME COMPLETE!", True, Colors.TEXT_HIGHLIGHT)
    title_rect = title.get_rect(center=(550, 100))
    screen.blit(title, title_rect)
    
    # Summary
    summary_lines = [
        "Progressive Learning System:",
        "",
        "Level 1 (Easy): Basic treasure hunting",
        "• Simple step-by-step navigation",
        "• Clear visibility of entire maze",
        "• Learn fundamental movement commands",
        "",
        "Level 2 (Intermediate): Pattern recognition", 
        "• Encourage loop-based solutions",
        "• Challenge: solve in 5 lines or less",
        "• Develop algorithmic thinking",
        "",
        "Level 3 (Advanced): A* pathfinding",
        "• Fog of war - can't see entire maze",
        "• Randomized mazes each time",
        "• A* algorithm visualization available",
        "• Real pathfinding challenge",
        "",
        "Features implemented:",
        "✅ Progressive difficulty unlocking",
        "✅ Fog of war system",
        "✅ A* algorithm visualization", 
        "✅ Educational code templates",
        "✅ Performance tracking & scoring"
    ]
    
    y_offset = 150
    for line in summary_lines:
        if line.startswith("Level"):
            color = Colors.TEXT_HIGHLIGHT
            font_to_use = medium_font
        elif line.startswith("✅"):
            color = (0, 255, 0)
            font_to_use = small_font
        elif line.startswith("•"):
            color = (200, 200, 200)
            font_to_use = small_font
        else:
            color = Colors.TEXT
            font_to_use = small_font
            
        text_surface = font_to_use.render(line, True, color)
        screen.blit(text_surface, (50, y_offset))
        y_offset += 25
    
    pg.display.flip()
    
    # Wait for user input
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
            elif event.type == pg.KEYDOWN:
                waiting = False
        clock.tick(60)
    
    pg.quit()
    
    print("\n" + "=" * 60)
    print("🎮 MAZE GAME DEMO SUMMARY")
    print("=" * 60)
    print("Educational Features:")
    print("• 📚 Progressive difficulty (Easy → Intermediate → Advanced)")
    print("• 🔒 Level unlocking system encourages completion")
    print("• 🌫️ Fog of war prevents brute-force solutions")
    print("• 🔍 A* visualization teaches algorithms")
    print("• 💎 Treasure chest visual motivation")
    print("• 🏆 Big score display with performance rating")
    print("• 🎯 Step counting focus on efficiency")
    print("• 📝 Level-specific code templates")
    print("• 🎲 Randomized mazes for replayability")
    print("\nReady for your hackathon demo! 🚀")

if __name__ == "__main__":
    try:
        demo_level_progression()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Demo completed.")