"""
Demo script showing the text editor functionality
"""

# This script demonstrates the embedded text editor!
# You can:
# - Type directly in the editor window
# - Use arrow keys to move cursor
# - Use Home/End to jump to line start/end
# - Use Backspace/Delete to edit text
# - Press Ctrl+Enter to execute code
# - Press Ctrl+R to reset the level

# Try editing this code and running it:
print("Hello from the embedded editor!")

# Basic movement commands:
forward(2)
right()
forward(3)

# Smart pathfinding loop:
for step in range(15):  # Safety limit
    if at_goal():
        print("Reached the goal!")
        break
    
    if scan() == "WALL":
        right()
        print("Turned right to avoid wall")
    else:
        forward(1)
        print("Moved forward")

print("Algorithm complete!")