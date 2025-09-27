"""
Menu System for Maze Game
------------------------

Handles the home screen, level selection, and username management.
"""
import pygame as pg
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import importlib.util
from engine.renderer import Colors
from leaderboard import leaderboard

class MenuButton:
    def __init__(self, rect: pg.Rect, text: str, action: callable, 
                 bg_color: Tuple[int, int, int] = (40, 40, 50),
                 hover_color: Tuple[int, int, int] = (60, 60, 70)):
        self.rect = rect
        self.text = text
        self.action = action
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False
        self.rect = rect
        self.text = text
        self.action = action
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, screen: pg.Surface, font: pg.font.Font):
        # Draw button background with rounded corners effect
        color = self.hover_color if self.is_hovered else self.bg_color
        pg.draw.rect(screen, color, self.rect, border_radius=8)
        
        # Draw border (thicker when hovered)
        border_thickness = 3 if self.is_hovered else 2
        border_color = (100, 100, 255) if self.is_hovered else (70, 70, 100)
        pg.draw.rect(screen, border_color, self.rect, border_thickness, border_radius=8)
        
        # Draw text with shadow effect
        if self.is_hovered:
            # Draw shadow text
            shadow_surface = font.render(self.text, True, (0, 0, 0))
            shadow_rect = shadow_surface.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
            screen.blit(shadow_surface, shadow_rect)
        
        # Draw main text
        text_color = (255, 255, 255) if self.is_hovered else (200, 200, 200)
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event: pg.event.Event) -> bool:
        if event.type == pg.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()
                return True
        return False

class TextInput:
    def __init__(self, rect: pg.Rect, placeholder: str = ""):
        self.rect = rect
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def draw(self, screen: pg.Surface, font: pg.font.Font):
        # Draw background
        color = Colors.GRAY if self.active else Colors.DARK_GRAY
        pg.draw.rect(screen, color, self.rect)
        pg.draw.rect(screen, Colors.TEXT, self.rect, 2 if self.active else 1)
        
        # Draw text or placeholder
        if self.text:
            text_surface = font.render(self.text, True, Colors.TEXT)
        else:
            text_surface = font.render(self.placeholder, True, Colors.GRAY)
        
        # Center text vertically, align left with padding
        text_rect = text_surface.get_rect(
            midleft=(self.rect.left + 10, self.rect.centery)
        )
        screen.blit(text_surface, text_rect)
        
        # Draw cursor when active
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            if cursor_x < self.rect.right - 5:
                pg.draw.line(screen, Colors.TEXT,
                           (cursor_x, self.rect.centery - 8),
                           (cursor_x, self.rect.centery + 8), 2)
    
    def handle_event(self, event: pg.event.Event) -> bool:
        if event.type == pg.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_RETURN:
                self.active = False
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 20:  # Maximum length
                    self.text += event.unicode
            return True
        return False
    
    def update(self, dt: float):
        self.cursor_timer += dt
        if self.cursor_timer >= 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

class MenuSystem:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.font = pg.font.Font(None, 32)
        self.small_font = pg.font.Font(None, 24)
        self.current_menu = "home"  # "home" or "level_select"
        
        # Load levels first
        self.levels = self.find_levels()
        
        # Create buttons and input fields
        screen_center_x = screen.get_width() // 2
        
        # Username input
        self.username_input = TextInput(
            pg.Rect(screen_center_x - 150, 200, 300, 40),
            "Enter username..."
        )
        
        # Menu buttons
        button_width = 200
        button_height = 50
        button_y = 300
        
        self.start_button = MenuButton(
            pg.Rect(screen_center_x - button_width//2, button_y, 
                   button_width, button_height),
            "Start Game",
            self.start_game
        )
        
        # Load available levels
        self.levels = self.find_levels()
        self.level_buttons = []
        
        # Create level selection buttons
        print("Creating level buttons...")
        self.level_buttons = []
        for i, level in enumerate(self.levels):
            print(f"Creating button for level {i+1}: {level.name}")
            # Center buttons vertically in the screen
            total_height = len(self.levels) * 70  # 70 pixels per button
            start_y = (screen.get_height() - total_height) // 2
            y_pos = start_y + i*70
            
            def make_action(lvl):
                return lambda: self.select_level(lvl)
            
            button = MenuButton(
                pg.Rect(screen_center_x - button_width//2, y_pos, button_width, button_height),
                f"Level {i+1}: {level.name}",
                make_action(level)
            )
            self.level_buttons.append(button)
            print(f"Added button at y={y_pos} for {level.name}")
        
        self.back_button = MenuButton(
            pg.Rect(50, 50, 100, 40),
            "Back",
            self.show_home
        )
        
        self.selected_level = None
    
    def find_levels(self) -> List:
        """Find and load all available level modules"""
        levels = []
        
        # Import level modules directly
        from levels.level1_basics import Level1
        from levels.level2_scanner import Level2
        from levels.level3_loops import Level3
        from levels.level4_algorithm import Level4
        
        # Create instances of each level
        level_classes = [Level1, Level2, Level3, Level4]
        
        for i, level_class in enumerate(level_classes, 1):
            try:
                level = level_class()
                print(f"Loading Level {i}: {level.name}")
                levels.append(level)
            except Exception as e:
                print(f"Error loading Level {i}: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"Total levels loaded: {len(levels)}")
        return levels
    
    def show_home(self):
        """Switch to home menu"""
        self.current_menu = "home"
        
    def show_level_select(self):
        """Switch to level select menu"""
        if not self.username_input.text.strip():
            # Don't proceed without username
            return
        self.current_menu = "level_select"
        
    def select_level(self, level) -> Optional[object]:
        """Select a level and return it"""
        print(f"Level selected: {level.name}")
        self.selected_level = level
        return level
    
    def start_game(self):
        """Start button clicked - proceed to level select"""
        if self.username_input.text.strip():
            # Save username
            leaderboard.username = self.username_input.text.strip()
            self.show_level_select()
    
    def handle_event(self, event: pg.event.Event) -> Optional[object]:
        """Handle events and return selected level if one is chosen"""
        if self.current_menu == "home":
            self.username_input.handle_event(event)
            self.start_button.handle_event(event)
            
        elif self.current_menu == "level_select":
            self.back_button.handle_event(event)
            for button in self.level_buttons:
                if button.handle_event(event):
                    return self.selected_level
        
        return None
    
    def update(self, dt: float):
        """Update animations"""
        self.username_input.update(dt)
    
    def draw(self):
        """Draw the current menu"""
        self.screen.fill(Colors.EDITOR_BG)
        
        if self.current_menu == "home":
            # Draw title
            title = self.font.render("Maze Algorithm Learning Platform", True, Colors.TEXT_HIGHLIGHT)
            title_rect = title.get_rect(centerx=self.screen.get_width()//2, y=100)
            self.screen.blit(title, title_rect)
            
            # Draw input field
            self.username_input.draw(self.screen, self.font)
            
            # Draw start button
            self.start_button.draw(self.screen, self.font)
            
        elif self.current_menu == "level_select":
            # Draw title
            title = self.font.render("Select Level", True, Colors.TEXT_HIGHLIGHT)
            title_rect = title.get_rect(centerx=self.screen.get_width()//2, y=50)
            self.screen.blit(title, title_rect)
            
            # Draw back button
            self.back_button.draw(self.screen, self.small_font)
            
            # Show current username
            username_text = self.small_font.render(f"Player: {self.username_input.text}", True, Colors.TEXT)
            self.screen.blit(username_text, (10, 10))
            
            # Draw level buttons and descriptions
            if not self.level_buttons:
                no_levels = self.font.render("No levels found!", True, Colors.TEXT_HIGHLIGHT)
                self.screen.blit(no_levels, (self.screen.get_width()//2 - 100, 200))
            else:
                for i, button in enumerate(self.level_buttons):
                    button.draw(self.screen, self.font)
                    # Draw level description below button if hovered
                    if button.is_hovered and i < len(self.levels):
                        desc = self.small_font.render(self.levels[i].description, True, Colors.TEXT)
                        desc_rect = desc.get_rect(midtop=(button.rect.centerx, button.rect.bottom + 5))
                        self.screen.blit(desc, desc_rect)