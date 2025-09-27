"""
Text Editor Tests
---------------

Verification suite for the text editor component. Tests basic
functionality and user interactions.

Tests:
- Basic typing and cursor movement
- Special key handling (arrows, backspace, etc)
- Syntax highlighting
- Copy/paste operations
- Multi-line editing

Run this file directly to execute tests:
    python test_editor.py
"""
import pygame as pg
import sys
from engine.editor import TextEditor

def test_text_editor():
    pg.init()
    
    # Small test window
    screen = pg.display.set_mode((600, 400))
    pg.display.set_caption("Text Editor Test")
    clock = pg.time.Clock()
    
    # Create text editor
    font = pg.font.Font(None, 20)
    editor_rect = pg.Rect(10, 10, 580, 350)
    editor = TextEditor(editor_rect, font)
    
    # Set some test text
    editor.set_text("""# Test the text editor!
# Try typing, arrow keys, backspace, etc.

def test_function():
    print("Hello World!")
    for i in range(5):
        print(f"Count: {i}")

# This demonstrates syntax highlighting
if True:
    test_function()
""")
    
    print("Text editor test running...")
    print("Try typing, using arrow keys, backspace, etc.")
    print("Press ESC to exit")
    
    running = True
    while running:
        dt = clock.tick(60) / 1000
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            else:
                editor.handle_event(event)
        
        editor.update(dt)
        
        screen.fill((30, 30, 30))
        editor.draw(screen)
        
        # Show current text in console every 5 seconds
        if int(pg.time.get_ticks() / 5000) > int((pg.time.get_ticks() - dt*1000) / 5000):
            print("Current text:")
            print(repr(editor.get_text()))
            print("---")
        
        pg.display.flip()
    
    pg.quit()
    print("Text editor test complete!")

if __name__ == "__main__":
    test_text_editor()