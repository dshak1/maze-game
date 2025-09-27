"""
Leaderboard System
-----------------

Handles score tracking and persistence for the maze game.
Maintains separate leaderboards for each level and supports
multiple users.

Features:
- Per-level leaderboards
- Top 10 scores per level
- Username management
- Score persistence using JSON files
- Best score tracking per user

Usage:
    from game.leaderboard import leaderboard

    # Set the current player's username
    leaderboard.username = "player1"

    # Add a score for level 1
    leaderboard.add_score(level=1, score=100)

    # Get all scores for level 1
    scores = leaderboard.get_scores(level=1)

    # Get player's best score
    best = leaderboard.get_user_best_score(level=1)
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Tuple

class Leaderboard:
    def __init__(self):
        self.data_dir = Path(__file__).parent / 'data'
        self.data_dir.mkdir(exist_ok=True)
        self._current_username = ""

    @property
    def username(self) -> str:
        """Get the current username."""
        return self._current_username

    @username.setter
    def username(self, value: str):
        """Set the current username."""
        self._current_username = value.strip()

    def _get_leaderboard_path(self, level: int) -> Path:
        """Get the path to the leaderboard file for a specific level."""
        return self.data_dir / f'leaderboard_level_{level}.json'

    def add_score(self, level: int, score: int) -> bool:
        """
        Add a score to the leaderboard for a specific level.
        
        Args:
            level: The level number
            score: The score achieved
            
        Returns:
            bool: True if the score was added successfully
        """
        if not self.username:
            return False

        file_path = self._get_leaderboard_path(level)
        scores = self.get_scores(level)
        
        # Add new score
        scores.append((self.username, score))
        # Sort by score (lower is better)
        scores.sort(key=lambda x: x[1])
        # Keep only top 10 scores
        scores = scores[:10]

        # Save to file
        with open(file_path, 'w') as f:
            json.dump(scores, f)

        return True

    def get_scores(self, level: int) -> List[Tuple[str, int]]:
        """
        Get all scores for a specific level.
        
        Args:
            level: The level number
            
        Returns:
            List of (username, score) tuples, sorted by score
        """
        file_path = self._get_leaderboard_path(level)
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_user_best_score(self, level: int) -> int:
        """
        Get the best score for the current user on a specific level.
        
        Args:
            level: The level number
            
        Returns:
            The best score or -1 if no score exists
        """
        if not self.username:
            return -1

        scores = self.get_scores(level)
        user_scores = [score for name, score in scores if name == self.username]
        return min(user_scores) if user_scores else -1

# Create a global instance
leaderboard = Leaderboard()
