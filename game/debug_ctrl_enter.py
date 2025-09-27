#!/usr/bin/env python3
"""
Debug test for Ctrl+Enter event handling
"""
import pygame as pg
import sys
from engine.editor import TextEditor

def test_ctrl_enter():
    print("🧪 TESTING CTRL+ENTER EVENT HANDLING")
    print("=" * 50)
    print("Instructions:")
    print("1. Type some text in the editor")
    print("2. Press Ctrl+Enter to test")
    print("3. Press ESC to exit")
    print("=" * 50)
    
    # Initialize pygame
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Ctrl+Enter Debug Test")
    clock = pg.time.Clock()
    
    # Create text editor
    font = pg.font.Font(None, 20)
    editor_rect = pg.Rect(50, 50, 700, 400)
    text_editor = TextEditor(editor_rect, font)
    
    # Set initial text
    text_editor.set_text("# Type your code here\n# Then press Ctrl+Enter\nforward(5)\nright()\nforward(3)")
    
    running = True
    ctrl_enter_count = 0
    
    while running:
        dt = clock.tick(60) / 1000
        
        for event in pg.event.get():
            # Debug: Print all keydown events
            if event.type == pg.KEYDOWN:
                mods = pg.key.get_pressed()
                ctrl_pressed = mods[pg.K_LCTRL] or mods[pg.K_RCTRL]
                print(f"Key pressed: {pg.key.name(event.key)}, Ctrl: {ctrl_pressed}")
            
            # Let text editor handle events first
            editor_consumed = text_editor.handle_event(event)
            print(f"Editor consumed event: {editor_consumed}")
            
            if editor_consumed:
                continue  # Event was consumed by editor
                
            if event.type == pg.QUIT:
                print("Quit event received")
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    print("ESC pressed - exiting")
                    running = False
                elif event.key == pg.K_RETURN and pg.key.get_pressed()[pg.K_LCTRL]:
                    # Ctrl+Enter - This should work!
                    ctrl_enter_count += 1
                    print(f"🎉 CTRL+ENTER DETECTED! (Count: {ctrl_enter_count})")
                    print(f"Code to execute:\n{text_editor.get_text()}")
                    print("-" * 30)
        
        # Update
        text_editor.update(dt)
        
        # Draw
        screen.fill((30, 30, 30))
        
        # Draw editor
        text_editor.draw(screen)
        
        # Draw status
        font_big = pg.font.Font(None, 36)
        status_text = f"Ctrl+Enter count: {ctrl_enter_count}"
        status_color = (0, 255, 0) if ctrl_enter_count > 0 else (255, 255, 255)
        status_surface = font_big.render(status_text, True, status_color)
        screen.blit(status_surface, (50, 500))
        
        # Draw instructions
        font_small = pg.font.Font(None, 24)
        instructions = [
            "Type in the editor above",
            "Press Ctrl+Enter to test execution",
            "Press ESC to exit"
        ]
        
        y_offset = 520
        for instruction in instructions:
            text_surface = font_small.render(instruction, True, (200, 200, 200))
            screen.blit(text_surface, (50, y_offset))
            y_offset += 25
        
        pg.display.flip()
    
    pg.quit()
    
    print(f"\nTest Results:")
    print(f"Total Ctrl+Enter detections: {ctrl_enter_count}")
    if ctrl_enter_count > 0:
        print("✅ Ctrl+Enter is working!")
    else:
        print("❌ Ctrl+Enter not detected - there's an issue")

if __name__ == "__main__":
    try:
        test_ctrl_enter()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()