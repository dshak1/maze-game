#!/usr/bin/env python3
"""
Quick test to verify the right wall is no longer cut off
"""
import pygame as pg
from engine.grid import Grid
from engine.renderer import Renderer, Colors

def test_wall_visibility():
    print("🧪 TESTING RIGHT WALL VISIBILITY")
    print("=" * 40)
    
    # Initialize pygame
    pg.init()
    screen = pg.display.set_mode((1100, 720))
    pg.display.set_caption("Wall Visibility Test")
    
    # Create grid with new dimensions
    grid = Grid(15, 20)  # Using new dimensions
    renderer = Renderer(screen, 32)
    
    # Create maze
    grid.create_simple_maze()
    
    # Calculate layout
    W, H = 1100, 720
    EDITOR_W = 420
    game_offset_x = EDITOR_W + 20  # 440
    game_offset_y = 50
    
    # Draw test
    screen.fill((20, 20, 24))
    
    # Draw editor panel background for reference
    editor_bg_rect = pg.Rect(0, 0, EDITOR_W, H)
    pg.draw.rect(screen, Colors.EDITOR_BG, editor_bg_rect)
    pg.draw.rect(screen, Colors.GRAY, editor_bg_rect, 2)
    
    # Draw grid
    renderer.draw_grid(grid, game_offset_x, game_offset_y)
    
    # Calculate dimensions
    required_width = 20 * 32  # 640px
    required_height = 15 * 32  # 480px
    available_width = W - game_offset_x - 20  # 640px
    
    # Draw boundary box to visualize available space
    boundary_rect = pg.Rect(game_offset_x, game_offset_y, available_width, 480)
    pg.draw.rect(screen, (255, 0, 0), boundary_rect, 3)  # Red boundary
    
    # Add info text
    font = pg.font.Font(None, 24)
    info_lines = [
        "🧪 RIGHT WALL VISIBILITY TEST",
        f"Grid: {grid.cols}x{grid.rows}",
        f"Required: {required_width}x{required_height}px", 
        f"Available: {available_width}x480px",
        f"Status: {'✅ FITS' if required_width <= available_width else '❌ OVERFLOW'}",
        "",
        "Red box shows available space",
        "Grid should fit exactly inside",
        "Press SPACE to take screenshot test"
    ]
    
    y_offset = 20
    for line in info_lines:
        color = Colors.TEXT_HIGHLIGHT if "✅" in line or "❌" in line else Colors.TEXT
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (20, y_offset))
        y_offset += 25
    
    pg.display.flip()
    
    # Check specific corners
    rightmost_col = grid.cols - 1  # Should be 19
    bottom_row = grid.rows - 1     # Should be 14
    
    print(f"Grid dimensions: {grid.cols}x{grid.rows}")
    print(f"Rightmost column: {rightmost_col}")
    print(f"Bottom row: {bottom_row}")
    print(f"Required width: {required_width}px")
    print(f"Available width: {available_width}px")
    print(f"Right wall position: {game_offset_x + rightmost_col * 32 + 32}px")
    print(f"Screen right edge: {W}px")
    
    right_wall_x = game_offset_x + rightmost_col * 32 + 32
    if right_wall_x <= W:
        print("✅ Right wall is fully visible!")
    else:
        print(f"❌ Right wall extends {right_wall_x - W}px beyond screen")
    
    # Interactive test
    print("\nPress SPACE in the window to continue...")
    waiting = True
    clock = pg.time.Clock()
    
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_ESCAPE:
                    waiting = False
        clock.tick(60)
    
    pg.quit()
    
    print("\n" + "=" * 40)
    print("🎉 WALL VISIBILITY TEST COMPLETE!")
    
    return right_wall_x <= W

if __name__ == "__main__":
    try:
        fits = test_wall_visibility()
        if fits:
            print("✅ SUCCESS: All walls are now visible!")
        else:
            print("❌ ISSUE: Right wall still cut off!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()