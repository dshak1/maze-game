#!/usr/bin/env python3
"""
Updated debug test for Ctrl+Enter event handling with proper modifier detection
"""
import pygame as pg
import sys
from engine.editor import TextEditor

def test_ctrl_enter_fixed():
    print("🧪 TESTING FIXED CTRL+ENTER EVENT HANDLING")
    print("=" * 50)
    print("Instructions:")
    print("1. Type some text in the editor")
    print("2. Press Ctrl+Enter to test")
    print("3. Watch for debug output")
    print("4. Press ESC to exit")
    print("=" * 50)
    
    # Initialize pygame
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Fixed Ctrl+Enter Debug Test")
    clock = pg.time.Clock()
    
    # Create text editor
    font = pg.font.Font(None, 20)
    editor_rect = pg.Rect(50, 50, 700, 400)
    text_editor = TextEditor(editor_rect, font)
    
    # Set initial text
    text_editor.set_text("# Test: Press Ctrl+Enter to execute!\nforward(5)\nright()\nforward(3)")
    
    running = True
    ctrl_enter_count = 0
    
    while running:
        dt = clock.tick(60) / 1000
        
        for event in pg.event.get():
            # Debug: Print all keydown events with modifiers
            if event.type == pg.KEYDOWN:
                ctrl_mod = event.mod & pg.KMOD_CTRL
                print(f"Key: {pg.key.name(event.key)}, Ctrl mod: {bool(ctrl_mod)}, event.mod: {event.mod}")
            
            # Let text editor handle events first
            editor_consumed = text_editor.handle_event(event)
            if editor_consumed:
                print(f"Editor consumed: {pg.key.name(event.key) if event.type == pg.KEYDOWN else 'non-key'}")
                continue  # Event was consumed by editor
                
            if event.type == pg.QUIT:
                print("Quit event received")
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    print("ESC pressed - exiting")
                    running = False
                elif event.key == pg.K_RETURN and (event.mod & pg.KMOD_CTRL):
                    # Fixed Ctrl+Enter detection!
                    ctrl_enter_count += 1
                    print(f"🎉 CTRL+ENTER DETECTED! (Count: {ctrl_enter_count})")
                    print(f"Code to execute:")
                    print(text_editor.get_text())
                    print("-" * 30)
                else:
                    print(f"Key not handled: {pg.key.name(event.key)}")
        
        # Update
        text_editor.update(dt)
        
        # Draw
        screen.fill((30, 30, 30))
        
        # Draw editor
        text_editor.draw(screen)
        
        # Draw status
        font_big = pg.font.Font(None, 36)
        status_text = f"Ctrl+Enter detections: {ctrl_enter_count}"
        status_color = (0, 255, 0) if ctrl_enter_count > 0 else (255, 255, 255)
        status_surface = font_big.render(status_text, True, status_color)
        screen.blit(status_surface, (50, 480))
        
        # Draw instructions
        font_small = pg.font.Font(None, 24)
        instructions = [
            "✅ FIXED VERSION - Using event.mod instead of get_pressed()",
            "Type in the editor, then press Ctrl+Enter",
            "Watch terminal for debug output",
            "Press ESC to exit"
        ]
        
        y_offset = 520
        for instruction in instructions:
            color = (100, 255, 100) if "FIXED" in instruction else (200, 200, 200)
            text_surface = font_small.render(instruction, True, color)
            screen.blit(text_surface, (50, y_offset))
            y_offset += 20
        
        pg.display.flip()
    
    pg.quit()
    
    print(f"\n🏁 Test Results:")
    print(f"Total Ctrl+Enter detections: {ctrl_enter_count}")
    if ctrl_enter_count > 0:
        print("✅ SUCCESS! Ctrl+Enter is now working!")
    else:
        print("❌ STILL BROKEN: Ctrl+Enter not detected")

if __name__ == "__main__":
    try:
        test_ctrl_enter_fixed()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()