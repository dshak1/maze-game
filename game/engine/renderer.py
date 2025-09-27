"""
Renderer System
--------------

Handles all visual aspects of the game including grid rendering,
agent visualization, UI elements, and algorithm visualization.

Features:
- Grid visualization with different tile types
- Agent rendering with direction indicator
- Pathfinding visualization (visited cells, distances)
- Path drawing for solution display
- Code editor panel rendering
- Statistics panel
- Color schemes for different game elements

Usage:
    from engine.renderer import Renderer, Colors
    
    screen = pygame.display.set_mode((800, 600))
    renderer = Renderer(screen, tile_size=32)

    # Draw game elements
    renderer.draw_grid(grid)
    renderer.draw_agent(agent)
    renderer.draw_pathfinding_overlay(grid)
    renderer.draw_stats_panel(stats_rect, stats)
"""
import pygame as pg
from typing import Dict, Optional, Tuple
from .grid import Grid, TileType, Tile
from .agent import Agent, Direction

class Colors:
    # Base colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (64, 64, 64)
    
    # Tile colors
    EMPTY = (240, 240, 240)
    WALL = (40, 40, 40)
    START = (100, 255, 100)
    GOAL = (255, 100, 100)
    AGENT = (0, 0, 255)
    
    # Weight colors
    ROAD = (200, 200, 200)      # cost 1
    SAND = (255, 255, 150)      # cost 3
    SWAMP = (100, 150, 100)     # cost 5
    
    # Algorithm visualization
    FRONTIER = (255, 255, 0, 128)    # yellow with alpha
    VISITED = (0, 255, 0, 128)       # green with alpha
    PATH = (255, 0, 255, 128)        # magenta with alpha
    
    # UI
    EDITOR_BG = (28, 28, 36)
    TEXT = (220, 220, 220)
    TEXT_HIGHLIGHT = (255, 255, 100)

class Renderer:
    def __init__(self, screen: pg.Surface, tile_size: int = 32):
        self.screen = screen
        self.tile_size = tile_size
        self.font = pg.font.Font(None, 24)
        self.small_font = pg.font.Font(None, 16)
        
        # Color mapping for tile types
        self.tile_colors = {
            TileType.EMPTY: Colors.EMPTY,
            TileType.WALL: Colors.WALL,
            TileType.START: Colors.START,
            TileType.GOAL: Colors.GOAL
        }
        
        # Weight colors based on cost
        self.weight_colors = {
            1: Colors.ROAD,
            3: Colors.SAND,
            5: Colors.SWAMP
        }
    
    def draw_grid(self, grid: Grid, offset_x: int = 0, offset_y: int = 0):
        """Draw the game grid with tiles"""
        for row in range(grid.rows):
            for col in range(grid.cols):
                tile = grid.tiles[row][col]
                x = offset_x + col * self.tile_size
                y = offset_y + row * self.tile_size
                
                # Choose tile color - simplified (no weights)
                color = self.tile_colors.get(tile.type, Colors.EMPTY)
                
                # Draw tile
                rect = pg.Rect(x, y, self.tile_size, self.tile_size)
                pg.draw.rect(self.screen, color, rect)
                pg.draw.rect(self.screen, Colors.BLACK, rect, 1)
                
                # Draw treasure chest on goal tile
                if tile.type == TileType.GOAL:
                    self.draw_treasure_chest(x, y)
    
    def draw_agent(self, agent: Agent, offset_x: int = 0, offset_y: int = 0):
        """Draw the agent with direction indicator"""
        x = offset_x + agent.col * self.tile_size
        y = offset_y + agent.row * self.tile_size
        
        center_x = x + self.tile_size // 2
        center_y = y + self.tile_size // 2
        
        # Draw agent circle
        pg.draw.circle(self.screen, Colors.AGENT, (center_x, center_y), self.tile_size // 3)
        pg.draw.circle(self.screen, Colors.WHITE, (center_x, center_y), self.tile_size // 3, 2)
        
        # Draw direction arrow
        arrow_text = self.font.render(agent.get_direction_symbol(), True, Colors.WHITE)
        arrow_rect = arrow_text.get_rect(center=(center_x, center_y))
        self.screen.blit(arrow_text, arrow_rect)
    
    def draw_treasure_chest(self, x: int, y: int):
        """Draw a treasure chest symbol on the goal tile"""
        center_x = x + self.tile_size // 2
        center_y = y + self.tile_size // 2
        size = self.tile_size // 3
        
        # Draw chest base (brown rectangle)
        chest_color = (139, 69, 19)  # Brown
        gold_color = (255, 215, 0)   # Gold
        
        # Main chest body
        chest_rect = pg.Rect(center_x - size, center_y - size//2, size * 2, size)
        pg.draw.rect(self.screen, chest_color, chest_rect)
        pg.draw.rect(self.screen, Colors.BLACK, chest_rect, 2)
        
        # Chest lid
        lid_rect = pg.Rect(center_x - size, center_y - size//2 - 4, size * 2, 8)
        pg.draw.rect(self.screen, chest_color, lid_rect)
        pg.draw.rect(self.screen, Colors.BLACK, lid_rect, 2)
        
        # Golden treasure symbol in center
        treasure_text = self.small_font.render("💎", True, gold_color)
        if treasure_text.get_width() == 0:  # Fallback if emoji not supported
            treasure_text = self.small_font.render("$", True, gold_color)
        treasure_rect = treasure_text.get_rect(center=(center_x, center_y))
        self.screen.blit(treasure_text, treasure_rect)
    
    def draw_pathfinding_overlay(self, grid: Grid, offset_x: int = 0, offset_y: int = 0, 
                                show_distances: bool = False, show_visited: bool = True):
        """Draw pathfinding visualization overlay"""
        for row in range(grid.rows):
            for col in range(grid.cols):
                tile = grid.tiles[row][col]
                x = offset_x + col * self.tile_size
                y = offset_y + row * self.tile_size
                
                # Create overlay surface with alpha
                overlay = pg.Surface((self.tile_size, self.tile_size), pg.SRCALPHA)
                
                # Color visited tiles
                if show_visited and tile.visited:
                    overlay.fill(Colors.VISITED)
                    self.screen.blit(overlay, (x, y))
                
                # Show distance values
                if show_distances and tile.distance != float('inf'):
                    dist_text = self.small_font.render(f"{tile.distance:.1f}", True, Colors.BLACK)
                    text_rect = dist_text.get_rect(center=(x + self.tile_size//2, y + self.tile_size//4))
                    self.screen.blit(dist_text, text_rect)
    
    def draw_path(self, path: list, offset_x: int = 0, offset_y: int = 0):
        """Draw the final path"""
        if len(path) < 2:
            return
        
        # Draw path segments
        for i in range(len(path) - 1):
            row1, col1 = path[i]
            row2, col2 = path[i + 1]
            
            x1 = offset_x + col1 * self.tile_size + self.tile_size // 2
            y1 = offset_y + row1 * self.tile_size + self.tile_size // 2
            x2 = offset_x + col2 * self.tile_size + self.tile_size // 2
            y2 = offset_y + row2 * self.tile_size + self.tile_size // 2
            
            pg.draw.line(self.screen, Colors.PATH[:3], (x1, y1), (x2, y2), 4)
    
    def draw_editor_panel(self, rect: pg.Rect, code_text: str = "", cursor_pos: int = 0):
        """Draw the code editor panel"""
        # Background
        pg.draw.rect(self.screen, Colors.EDITOR_BG, rect)
        pg.draw.rect(self.screen, Colors.GRAY, rect, 2)
        
        # Title
        title = self.font.render("Code Editor", True, Colors.TEXT_HIGHLIGHT)
        self.screen.blit(title, (rect.x + 10, rect.y + 10))
        
        # Code text area
        text_rect = pg.Rect(rect.x + 10, rect.y + 40, rect.width - 20, rect.height - 80)
        pg.draw.rect(self.screen, Colors.BLACK, text_rect)
        pg.draw.rect(self.screen, Colors.GRAY, text_rect, 1)
        
        if code_text:
            lines = code_text.split('\n')
            y_offset = text_rect.y + 5
            
            for line in lines:
                if y_offset < text_rect.bottom - 20:
                    text_surface = self.small_font.render(line, True, Colors.TEXT)
                    self.screen.blit(text_surface, (text_rect.x + 5, y_offset))
                    y_offset += 20
        
        # Instructions
        instructions = [
            "Controls:",
            "Ctrl+Enter - Run code",
            "Ctrl+R - Reset level",
            "",
            "Available functions:",
            "forward(n) - move n steps",
            "left() - turn left", 
            "right() - turn right",
            "scan() - check ahead",
            "at_goal() - check if at goal"
        ]
        
        y_offset = rect.bottom - 200
        for instruction in instructions:
            if y_offset < rect.bottom - 10:
                text_surface = self.small_font.render(instruction, True, Colors.TEXT)
                self.screen.blit(text_surface, (rect.x + 10, y_offset))
                y_offset += 16
    
    def draw_stats_panel(self, rect: pg.Rect, stats: Dict[str, any]):
        """Draw statistics panel showing steps and efficiency"""
        pg.draw.rect(self.screen, Colors.DARK_GRAY, rect)
        pg.draw.rect(self.screen, Colors.GRAY, rect, 2)
        
        title = self.font.render("Performance", True, Colors.TEXT_HIGHLIGHT)
        self.screen.blit(title, (rect.x + 10, rect.y + 10))
        
        y_offset = rect.y + 35
        for key, value in stats.items():
            text = f"{key}: {value}"
            color = Colors.TEXT_HIGHLIGHT if key == "Steps Taken" else Colors.TEXT
            text_surface = self.small_font.render(text, True, color)
            self.screen.blit(text_surface, (rect.x + 10, y_offset))
            y_offset += 18
    
    def draw_victory_screen(self, steps_taken: int, optimal_steps: int):
        """Draw a big victory message with score in the center of the screen"""
        screen_rect = self.screen.get_rect()
        
        # Semi-transparent overlay
        overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with transparency
        self.screen.blit(overlay, (0, 0))
        
        # Create large font for the score
        try:
            big_font = pg.font.Font(None, 72)
            medium_font = pg.font.Font(None, 48)
            small_font = pg.font.Font(None, 36)
        except:
            big_font = self.font
            medium_font = self.font
            small_font = self.font
        
        # Victory message
        victory_text = big_font.render("🏆 TREASURE FOUND! 🏆", True, Colors.TEXT_HIGHLIGHT)
        victory_rect = victory_text.get_rect(center=(screen_rect.centerx, screen_rect.centery - 120))
        self.screen.blit(victory_text, victory_rect)
        
        # Main score display
        score_text = f"SCORE: {steps_taken} STEPS"
        score_surface = medium_font.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(screen_rect.centerx, screen_rect.centery - 40))
        
        # Add a border/glow effect to the score
        border_surface = medium_font.render(score_text, True, (255, 215, 0))  # Gold border
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx != 0 or dy != 0:
                    border_rect = score_surface.get_rect(center=(screen_rect.centerx + dx, screen_rect.centery - 40 + dy))
                    self.screen.blit(border_surface, border_rect)
        
        self.screen.blit(score_surface, score_rect)
        
        # Performance comparison
        extra_steps = steps_taken - optimal_steps
        if extra_steps == 0:
            perf_text = "PERFECT! Optimal solution!"
            perf_color = (0, 255, 0)  # Green
        elif extra_steps <= 5:
            perf_text = f"Excellent! Only {extra_steps} extra steps"
            perf_color = (150, 255, 150)  # Light green
        elif extra_steps <= 10:
            perf_text = f"Good! {extra_steps} extra steps"
            perf_color = (255, 255, 0)  # Yellow
        else:
            perf_text = f"{extra_steps} extra steps (optimal: {optimal_steps})"
            perf_color = (255, 150, 150)  # Light red
        
        perf_surface = small_font.render(perf_text, True, perf_color)
        perf_rect = perf_surface.get_rect(center=(screen_rect.centerx, screen_rect.centery + 20))
        self.screen.blit(perf_surface, perf_rect)
        
        # Instructions
        instruction_text = "Press SPACE to continue or N for new maze"
        instruction_surface = self.small_font.render(instruction_text, True, Colors.TEXT)
        instruction_rect = instruction_surface.get_rect(center=(screen_rect.centerx, screen_rect.centery + 80))
        self.screen.blit(instruction_surface, instruction_rect)