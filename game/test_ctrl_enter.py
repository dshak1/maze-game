"""
Quick test to verify Ctrl+Enter handling
"""
import pygame as pg
from engine.editor import TextEditor

def test_ctrl_enter():
    pg.init()
    
    screen = pg.display.set_mode((400, 300))
    pg.display.set_caption("Ctrl+Enter Test")
    font = pg.font.Font(None, 20)
    
    editor = TextEditor(pg.Rect(10, 10, 380, 200), font)
    editor.set_text("# Try pressing Ctrl+Enter\nforward(1)\nright()")
    
    print("Test running:")
    print("- Type some text - should work")
    print("- Press Enter - should create new line")
    print("- Press Ctrl+Enter - should print 'CTRL+ENTER DETECTED' and NOT create new line") 
    print("- Press ESC to exit")
    
    clock = pg.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_RETURN and (pg.key.get_pressed()[pg.K_LCTRL]):
                    print("🎉 CTRL+ENTER DETECTED! (This should happen)")
                    print(f"Current text: {repr(editor.get_text())}")
                    continue
                
                # Let editor handle the event
                consumed = editor.handle_event(event)
                if consumed:
                    print(f"Editor consumed: {pg.key.name(event.key)}")
                else:
                    print(f"Editor did NOT consume: {pg.key.name(event.key)}")
        
        editor.update(dt)
        screen.fill((40, 40, 40))
        editor.draw(screen)
        pg.display.flip()
    
    pg.quit()
    print("Test complete!")

if __name__ == "__main__":
    test_ctrl_enter()