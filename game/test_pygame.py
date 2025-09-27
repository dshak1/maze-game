"""
Simple test version to debug issues
"""
import pygame as pg
import sys

def test_basic_pygame():
    """Test basic pygame functionality"""
    print("Testing basic pygame...")
    pg.init()
    
    # Small window for testing
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Test Window")
    clock = pg.time.Clock()
    
    print("Pygame initialized successfully")
    
    running = True
    frame_count = 0
    
    while running:
        frame_count += 1
        
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("Quit event received")
                running = False
            elif event.type == pg.KEYDOWN:
                print(f"Key pressed: {event.key}")
                if event.key == pg.K_ESCAPE:
                    running = False
        
        # Simple drawing
        screen.fill((50, 50, 50))
        
        # Draw a test rectangle
        pg.draw.rect(screen, (255, 0, 0), (100, 100, 200, 100))
        
        # Show frame count
        if frame_count % 60 == 0:  # Every second
            print(f"Frame: {frame_count}")
        
        pg.display.flip()
        clock.tick(60)  # 60 FPS
        
        # Safety exit after 10 seconds
        if frame_count > 600:
            print("Safety timeout reached")
            break
    
    print("Closing pygame...")
    pg.quit()
    print("Test complete!")

if __name__ == "__main__":
    test_basic_pygame()