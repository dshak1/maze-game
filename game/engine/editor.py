"""
Text Editor Widget
----------------

A full-featured text editor implementation in Pygame for code editing.
Provides syntax highlighting and modern text editing capabilities.

Features:
- Multi-line text editing
- Cursor movement and selection
- Syntax highlighting for Python
- Line numbers
- Auto-indentation
- Copy/paste support
- Scrolling for long content
- Custom color schemes

Usage:
    from engine.editor import TextEditor
    import pygame

    # Create editor
    font = pygame.font.Font(None, 20)
    editor = TextEditor(rect=pygame.Rect(10, 10, 400, 300), font=font)

    # Set initial content
    editor.set_text('# Write your code here\n')

    # In game loop:
    for event in pygame.event.get():
        if editor.handle_event(event):
            continue  # Event was handled by editor

    editor.update(dt)
    editor.draw(screen)
"""
import pygame as pg
from typing import List, Tuple, Optional

class TextEditor:
    def __init__(self, rect: pg.Rect, font: pg.font.Font, bg_color=(40, 40, 40), 
                 text_color=(220, 220, 220), cursor_color=(255, 255, 255)):
        self.rect = rect
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.cursor_color = cursor_color
        
        # Text state
        self.lines = [""]  # Start with one empty line
        self.cursor_row = 0
        self.cursor_col = 0
        self.scroll_y = 0
        
        # Visual settings
        self.line_height = font.get_height() + 2
        self.margin = 8
        self.tab_size = 4
        
        # Cursor animation
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_time = 500  # milliseconds
        
        # Selection (for future enhancement)
        self.selection_start = None
        self.selection_end = None
        
        # Keywords for basic syntax highlighting
        self.keywords = {
            'forward', 'left', 'right', 'scan', 'at_goal',
            'if', 'else', 'elif', 'while', 'for', 'def', 'return',
            'True', 'False', 'None', 'and', 'or', 'not', 'in'
        }
        self.keyword_color = (100, 150, 255)  # Light blue
        self.comment_color = (100, 150, 100)  # Light green
        self.string_color = (255, 200, 100)   # Light orange
    
    def get_text(self) -> str:
        """Get all text as a single string"""
        return '\n'.join(self.lines)
    
    def set_text(self, text: str):
        """Set the editor text"""
        self.lines = text.split('\n')
        if not self.lines:
            self.lines = [""]
        self.cursor_row = 0
        self.cursor_col = 0
        self.scroll_y = 0
    
    def handle_event(self, event: pg.event.Event) -> bool:
        """
        Handle pygame events. Returns True if event was consumed
        """
        if event.type == pg.KEYDOWN:
            # Let Ctrl+ combinations pass through to main game (except for future editor shortcuts)
            if event.mod & pg.KMOD_CTRL:
                # For now, let all Ctrl+ combinations pass through
                # In the future, we can handle Ctrl+C, Ctrl+V, etc. here
                return False  # Don't consume Ctrl+ events
            
            # Handle special keys (only without Ctrl modifier)
            if event.key == pg.K_RETURN:
                self._insert_newline()
                return True
            elif event.key == pg.K_BACKSPACE:
                self._handle_backspace()
                return True
            elif event.key == pg.K_DELETE:
                self._handle_delete()
                return True
            elif event.key == pg.K_TAB:
                self._insert_text('    ')  # 4 spaces for tab
                return True
            elif event.key == pg.K_LEFT:
                self._move_cursor_left()
                return True
            elif event.key == pg.K_RIGHT:
                self._move_cursor_right()
                return True
            elif event.key == pg.K_UP:
                self._move_cursor_up()
                return True
            elif event.key == pg.K_DOWN:
                self._move_cursor_down()
                return True
            elif event.key == pg.K_HOME:
                self.cursor_col = 0
                return True
            elif event.key == pg.K_END:
                self.cursor_col = len(self.lines[self.cursor_row])
                return True
            # Handle regular text input
            elif event.unicode and event.unicode.isprintable():
                self._insert_text(event.unicode)
                return True
        
        return False
    
    def _insert_text(self, text: str):
        """Insert text at cursor position"""
        line = self.lines[self.cursor_row]
        self.lines[self.cursor_row] = line[:self.cursor_col] + text + line[self.cursor_col:]
        self.cursor_col += len(text)
        self._ensure_cursor_visible()
    
    def _insert_newline(self):
        """Insert a new line at cursor position"""
        line = self.lines[self.cursor_row]
        
        # Split the current line at cursor
        left_part = line[:self.cursor_col]
        right_part = line[self.cursor_col:]
        
        # Auto-indent: preserve leading whitespace from current line
        indent = ''
        for char in left_part:
            if char in ' \t':
                indent += char
            else:
                break
        
        # Update lines
        self.lines[self.cursor_row] = left_part
        self.lines.insert(self.cursor_row + 1, indent + right_part)
        
        # Move cursor to new line
        self.cursor_row += 1
        self.cursor_col = len(indent)
        self._ensure_cursor_visible()
    
    def _handle_backspace(self):
        """Handle backspace key"""
        if self.cursor_col > 0:
            # Delete character before cursor
            line = self.lines[self.cursor_row]
            self.lines[self.cursor_row] = line[:self.cursor_col-1] + line[self.cursor_col:]
            self.cursor_col -= 1
        elif self.cursor_row > 0:
            # Join with previous line
            prev_line = self.lines[self.cursor_row - 1]
            current_line = self.lines[self.cursor_row]
            self.lines[self.cursor_row - 1] = prev_line + current_line
            del self.lines[self.cursor_row]
            self.cursor_row -= 1
            self.cursor_col = len(prev_line)
        self._ensure_cursor_visible()
    
    def _handle_delete(self):
        """Handle delete key"""
        line = self.lines[self.cursor_row]
        if self.cursor_col < len(line):
            # Delete character after cursor
            self.lines[self.cursor_row] = line[:self.cursor_col] + line[self.cursor_col+1:]
        elif self.cursor_row < len(self.lines) - 1:
            # Join with next line
            next_line = self.lines[self.cursor_row + 1]
            self.lines[self.cursor_row] = line + next_line
            del self.lines[self.cursor_row + 1]
    
    def _move_cursor_left(self):
        """Move cursor left"""
        if self.cursor_col > 0:
            self.cursor_col -= 1
        elif self.cursor_row > 0:
            self.cursor_row -= 1
            self.cursor_col = len(self.lines[self.cursor_row])
        self._ensure_cursor_visible()
    
    def _move_cursor_right(self):
        """Move cursor right"""
        line = self.lines[self.cursor_row]
        if self.cursor_col < len(line):
            self.cursor_col += 1
        elif self.cursor_row < len(self.lines) - 1:
            self.cursor_row += 1
            self.cursor_col = 0
        self._ensure_cursor_visible()
    
    def _move_cursor_up(self):
        """Move cursor up"""
        if self.cursor_row > 0:
            self.cursor_row -= 1
            # Clamp cursor column to line length
            line_len = len(self.lines[self.cursor_row])
            self.cursor_col = min(self.cursor_col, line_len)
        self._ensure_cursor_visible()
    
    def _move_cursor_down(self):
        """Move cursor down"""
        if self.cursor_row < len(self.lines) - 1:
            self.cursor_row += 1
            # Clamp cursor column to line length
            line_len = len(self.lines[self.cursor_row])
            self.cursor_col = min(self.cursor_col, line_len)
        self._ensure_cursor_visible()
    
    def _ensure_cursor_visible(self):
        """Scroll to ensure cursor is visible"""
        visible_lines = (self.rect.height - 2 * self.margin) // self.line_height
        
        # Scroll down if cursor is below visible area
        if self.cursor_row >= self.scroll_y + visible_lines:
            self.scroll_y = self.cursor_row - visible_lines + 1
        
        # Scroll up if cursor is above visible area
        if self.cursor_row < self.scroll_y:
            self.scroll_y = self.cursor_row
        
        # Ensure scroll_y is not negative
        self.scroll_y = max(0, self.scroll_y)
    
    def update(self, dt: float):
        """Update cursor blinking animation"""
        self.cursor_timer += dt * 1000  # Convert to milliseconds
        if self.cursor_timer >= self.cursor_blink_time:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def _highlight_syntax(self, text: str) -> List[Tuple[str, pg.Color]]:
        """
        Simple syntax highlighting - returns list of (text, color) tuples
        """
        result = []
        words = text.replace('\t', '    ').split(' ')
        
        for i, word in enumerate(words):
            if i > 0:
                result.append((' ', self.text_color))
            
            # Check for comments
            if '#' in word:
                comment_start = word.index('#')
                if comment_start > 0:
                    result.append((word[:comment_start], self.text_color))
                result.append((word[comment_start:], self.comment_color))
            # Check for keywords
            elif word.rstrip('():,') in self.keywords:
                result.append((word, self.keyword_color))
            # Check for strings (simple check)
            elif (word.startswith('"') and word.endswith('"')) or \
                 (word.startswith("'") and word.endswith("'")):
                result.append((word, self.string_color))
            else:
                result.append((word, self.text_color))
        
        return result
    
    def draw(self, screen: pg.Surface):
        """Draw the text editor"""
        # Draw background
        pg.draw.rect(screen, self.bg_color, self.rect)
        pg.draw.rect(screen, (100, 100, 100), self.rect, 2)
        
        # Calculate visible area
        text_rect = pg.Rect(
            self.rect.x + self.margin,
            self.rect.y + self.margin,
            self.rect.width - 2 * self.margin,
            self.rect.height - 2 * self.margin
        )
        
        visible_lines = text_rect.height // self.line_height
        start_line = self.scroll_y
        end_line = min(start_line + visible_lines, len(self.lines))
        
        # Draw line numbers
        line_num_width = 40
        line_num_rect = pg.Rect(text_rect.x, text_rect.y, line_num_width, text_rect.height)
        pg.draw.rect(screen, (50, 50, 50), line_num_rect)
        
        # Adjust text area for line numbers
        text_rect.x += line_num_width + 5
        text_rect.width -= line_num_width + 5
        
        # Draw lines
        y_offset = text_rect.y
        for line_idx in range(start_line, end_line):
            line_text = self.lines[line_idx]
            
            # Draw line number
            line_num = str(line_idx + 1).rjust(3)
            line_num_surface = self.font.render(line_num, True, (150, 150, 150))
            screen.blit(line_num_surface, (line_num_rect.x + 5, y_offset))
            
            # Draw line text with syntax highlighting
            x_offset = text_rect.x
            if line_text.strip():  # Only highlight non-empty lines
                highlighted = self._highlight_syntax(line_text)
                for text_part, color in highlighted:
                    if text_part:
                        text_surface = self.font.render(text_part, True, color)
                        screen.blit(text_surface, (x_offset, y_offset))
                        x_offset += text_surface.get_width()
            else:
                # Draw empty line (just for cursor positioning)
                text_surface = self.font.render(line_text, True, self.text_color)
                screen.blit(text_surface, (x_offset, y_offset))
            
            # Draw cursor if on this line
            if (line_idx == self.cursor_row and 
                self.cursor_visible and 
                start_line <= self.cursor_row < end_line):
                
                # Calculate cursor x position
                line_before_cursor = line_text[:self.cursor_col]
                cursor_x = text_rect.x + self.font.size(line_before_cursor)[0]
                cursor_y = y_offset
                
                # Draw cursor line
                pg.draw.line(screen, self.cursor_color, 
                           (cursor_x, cursor_y), 
                           (cursor_x, cursor_y + self.line_height - 2), 2)
            
            y_offset += self.line_height
        
        # Draw scrollbar if needed
        if len(self.lines) > visible_lines:
            self._draw_scrollbar(screen, visible_lines)
    
    def _draw_scrollbar(self, screen: pg.Surface, visible_lines: int):
        """Draw a simple scrollbar"""
        scrollbar_width = 12
        scrollbar_rect = pg.Rect(
            self.rect.right - scrollbar_width - 2,
            self.rect.y + 2,
            scrollbar_width,
            self.rect.height - 4
        )
        
        # Background
        pg.draw.rect(screen, (60, 60, 60), scrollbar_rect)
        
        # Thumb
        total_lines = len(self.lines)
        thumb_height = max(20, (visible_lines / total_lines) * scrollbar_rect.height)
        thumb_y = scrollbar_rect.y + (self.scroll_y / total_lines) * scrollbar_rect.height
        
        thumb_rect = pg.Rect(
            scrollbar_rect.x + 2,
            thumb_y,
            scrollbar_rect.width - 4,
            thumb_height
        )
        pg.draw.rect(screen, (120, 120, 120), thumb_rect)