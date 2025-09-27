"""
Renderer - handles all drawing operations for the game
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