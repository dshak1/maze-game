"""
Fog of War system for advanced maze levels
"""
import pygame as pg
from typing import Set, Tuple
from .grid import Grid, TileType

class FogOfWar:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.visible_tiles: Set[Tuple[int, int]] = set()
        self.vision_radius = 2  # How far agent can see
        self.explored_tiles: Set[Tuple[int, int]] = set()  # Previously seen tiles
        
    def update_vision(self, agent_row: int, agent_col: int):
        """Update visible tiles based on agent position"""
        # Agent can always see their current position
        self.visible_tiles.clear()
        self.visible_tiles.add((agent_row, agent_col))
        self.explored_tiles.add((agent_row, agent_col))
        
        # Add tiles within vision radius
        for dr in range(-self.vision_radius, self.vision_radius + 1):
            for dc in range(-self.vision_radius, self.vision_radius + 1):
                new_row = agent_row + dr
                new_col = agent_col + dc
                
                # Check bounds
                if (0 <= new_row < self.grid.rows and 
                    0 <= new_col < self.grid.cols):
                    
                    # Add to visible and explored
                    self.visible_tiles.add((new_row, new_col))
                    self.explored_tiles.add((new_row, new_col))
    
    def is_visible(self, row: int, col: int) -> bool:
        """Check if tile is currently visible"""
        return (row, col) in self.visible_tiles
    
    def is_explored(self, row: int, col: int) -> bool:
        """Check if tile has been explored before"""
        return (row, col) in self.explored_tiles
    
    def reset(self):
        """Reset fog of war"""
        self.visible_tiles.clear()
        self.explored_tiles.clear()

class FogRenderer:
    def __init__(self):
        # Fog colors
        self.fog_color = (40, 40, 60, 200)  # Dark blue with alpha
        self.explored_fog_color = (60, 60, 80, 120)  # Lighter for explored areas
        
    def draw_fog_overlay(self, screen: pg.Surface, grid: Grid, fog: FogOfWar, 
                        offset_x: int, offset_y: int, tile_size: int):
        """Draw fog overlay on the grid"""
        for row in range(grid.rows):
            for col in range(grid.cols):
                x = offset_x + col * tile_size
                y = offset_y + row * tile_size
                
                if not fog.is_visible(row, col):
                    # Create fog surface
                    fog_surface = pg.Surface((tile_size, tile_size), pg.SRCALPHA)
                    
                    if fog.is_explored(row, col):
                        # Previously explored - lighter fog
                        fog_surface.fill(self.explored_fog_color)
                    else:
                        # Unexplored - dense fog
                        fog_surface.fill(self.fog_color)
                    
                    screen.blit(fog_surface, (x, y))
                    
                    # Add fog pattern for visual effect
                    if not fog.is_explored(row, col):
                        # Draw question marks for unexplored areas
                        font = pg.font.Font(None, 24)
                        text = font.render("?", True, (150, 150, 150))
                        text_rect = text.get_rect(center=(x + tile_size//2, y + tile_size//2))
                        screen.blit(text, text_rect)
    
    def draw_vision_indicator(self, screen: pg.Surface, agent_row: int, agent_col: int,
                            fog: FogOfWar, offset_x: int, offset_y: int, tile_size: int):
        """Draw vision radius indicator around agent"""
        center_x = offset_x + agent_col * tile_size + tile_size // 2
        center_y = offset_y + agent_row * tile_size + tile_size // 2
        
        # Draw vision circle
        vision_radius_pixels = fog.vision_radius * tile_size
        pg.draw.circle(screen, (255, 255, 0, 50), 
                      (center_x, center_y), vision_radius_pixels, 2)