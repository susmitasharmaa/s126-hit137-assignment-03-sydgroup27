"""A class to represent the game user interface.
"""
import tkinter as tk
import numpy as np
from game_controller import GameController


class GameUI:
    """A class to represent the game UI.
    Attributes:
        root (tk.Tk): The main Tkinter window.
        original_canvas (tk.Canvas): Canvas displaying the original image.
        modified_canvas (tk.Canvas): Canvas displaying the modified image.
        remaining_label (tk.Label): Label showing remaining differences.
        mistakes_label (tk.Label): Label showing current mistakes.
        score_label (tk.Label): Label showing cumulative score.
        controller (GameController): The game controller that connects the UI and game logic.
    """
    root: tk.Tk
    original_canvas: tk.Canvas
    modified_canvas: tk.Canvas
    remaining_label: tk.Label
    mistakes_label: tk.Label
    score_label: tk.Label
    controller: GameController

    def __init__(self,  controller: GameController):
        """Initialises the Tkinter window and all UI elements.
        Note: modified_canvas click event must be bound to self.on_click here.
    """
        pass

    def load_image(self) -> None:
        """Opens file picker, loads selected image, starts new game."""

        # after image is picked, call controller function
        # self.controller.load_image(path)
        pass

    def display_images(self, original: np.ndarray, modified: np.ndarray) -> None:
        """Renders both images on their respective canvases."""
        pass

    def update_display(self, remaining: int, mistakes: int, score: int, found_regions: list, revealed_regions: list) -> None:
        """Updates labels and redraws circles on both canvases.
        Args:
            remaining: Number of differences still unfound.
            mistakes: Current mistake count.
            score: Cumulative score.
            found_regions: List of (x, y, w, h) tuples for found differences — draw red circles.
            revealed_regions: List of (x, y, w, h) tuples for revealed differences — draw blue circles.
        """
        pass

    def show_invalid_image_message(self) -> None:
        """Displays an error message if the loaded image is invalid."""
        pass

    def show_game_over(self, win: bool) -> None:
        """Displays game over message.
        Shows a popup message box with "You Win!" if win is True, or "Game Over!" if win is False.
        Args:
            win: True if player won, False if lost.
        """
        pass

    def draw_circle(self, canvas: tk.Canvas, x: int, y: int, radius: int, colour: str) -> None:
        """Draws a circle on the given canvas at image coordinates."""
        pass

    # Just calls game controller's handle_click() with the click coordinates
    # to update game state
    def on_click(self, event):
        self.controller.handle_click(event.x, event.y)
