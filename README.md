# Maze Algorithm Learning Platform

An interactive educational game that teaches algorithmic thinking through maze-solving challenges.

## Features

- Interactive code editor with syntax highlighting
- Real-time code execution and visualization
- Multiple levels with increasing complexity
- Leaderboard system for tracking progress
- Visual algorithm feedback
- Beginner-friendly interface

## Project Structure

```
maze-game/
├── game/
│   ├── engine/         # Core game engine components
│   │   ├── agent.py    # Player movement and actions
│   │   ├── grid.py     # Maze representation
│   │   ├── editor.py   # Code editor widget
│   │   ├── renderer.py # Visual rendering
│   │   └── runner.py   # Code execution sandbox
│   ├── levels/         # Level definitions
│   │   ├── level1_basics.py    # Introduction level
│   │   ├── level2_scanner.py   # Wall detection
│   │   ├── level3_loops.py     # Loop concepts
│   │   └── level4_algorithm.py # Advanced algorithms
│   ├── main.py         # Main game entry point
│   ├── menu.py         # Menu system
│   └── leaderboard.py  # Score tracking
└── tests/              # Test suite
```

## Getting Started

1. Install dependencies:
```bash
pip install pygame
```

2. Run the game:
```bash
python game/main.py
```

## How to Play

1. Enter your username on the home screen
2. Select a level from the menu
3. Write your solution in the code editor
4. Press Ctrl+Enter to run your code
5. Press Ctrl+R to reset the level
6. Use the back button to return to level selection

## Available Commands

In each level, you can use these commands:
- `forward(n)` - Move forward n steps
- `left()` - Turn left 90 degrees
- `right()` - Turn right 90 degrees
- `scan()` - Check what's ahead
- `at_goal()` - Check if at the goal

## Level Progression

1. **Basic Movement** - Learn fundamental commands
2. **Scanner Training** - Introduce wall detection
3. **Loop Master** - Practice using loops
4. **Algorithm Master** - Advanced problem-solving