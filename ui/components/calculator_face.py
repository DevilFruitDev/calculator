"""
Game-Style Calculator - Face Component
A reactive face that gives personality to the calculator
"""

import tkinter as tk
import random
from utils.styles import FACE_EXPRESSIONS, OPERATION_REACTIONS

class CalculatorFace:
    """
    A class to manage the calculator's facial expressions that react to user actions.
    This gives the calculator a personality and makes it more interactive.
    """
    
    def __init__(self, parent_frame, colors):
        """
        Initialize the calculator face display.
        
        Args:
            parent_frame: The tkinter frame to place the face in
            colors: Dictionary of color schemes from the main UI
        """
        self.parent = parent_frame
        self.colors = colors
        
        # Create a frame for the face
        self.face_frame = tk.Frame(
            self.parent,
            bg=self.colors["bg_medium"],
            bd=0
        )
        self.face_frame.pack(fill=tk.X, pady=0)
        
        # Create the face display label
        self.face_display = tk.Label(
            self.face_frame,
            text="🙂",  # Default emoji
            font=("Segoe UI Emoji", 24),  # Font with emoji support
            bg=self.colors["bg_medium"],
            fg=self.colors["accent1"],
            padx=10
        )
        self.face_display.pack(side=tk.RIGHT, padx=8)
        
        # Create a text bubble for reactions with emoji support
        self.bubble_frame = tk.Frame(
            self.face_frame,
            bg=self.colors["display_bg"],
            bd=2,
            relief=tk.RAISED
        )
        self.bubble_frame.pack(side=tk.RIGHT, padx=5)
        
        self.bubble_text = tk.Label(
            self.bubble_frame,
            text="Hello! 👋",
            font=("Segoe UI Emoji", 10),  # Font with emoji support
            bg=self.colors["display_bg"],
            fg=self.colors["accent2"],
            padx=5,
            pady=2
        )
        self.bubble_text.pack()
        
        # Initialize with welcome expression
        self.show_expression("happy", "Ready to calculate! ✨")
        
        # After a delay, hide the speech bubble
        self.parent.after(3000, self.hide_bubble)
    
    def show_expression(self, mood, message=""):
        """
        Show a facial expression and optional message.
        
        Args:
            mood (str): The mood to express (happy, sad, surprised, etc.)
            message (str): Optional message to display in bubble
        """
        # Get the expression or use default
        face = FACE_EXPRESSIONS.get(mood, FACE_EXPRESSIONS["default"])
        
        # Update the face display
        self.face_display.config(text=face)
        
        # If there's a message, show the bubble
        if message:
            self.bubble_text.config(text=message)
            self.bubble_frame.pack(side=tk.RIGHT, padx=5)
            
            # Auto-hide bubble after a few seconds
            self.parent.after(3000, self.hide_bubble)
        else:
            self.hide_bubble()
    
    def hide_bubble(self):
        """Hide the speech bubble."""
        self.bubble_frame.pack_forget()
    
    def react_to_calculation(self, result):
        """
        React to a calculation result.
        
        Args:
            result (str): The calculation result
        """
        try:
            # Convert to float to analyze the result
            value = float(result)
            
            # React based on the value
            if value == 42:
                self.show_expression("cool", "The answer!")
            elif value == 0:
                self.show_expression("thinking", "Zero...")
            elif value == 3.14159 or (3.14 <= value <= 3.15):
                self.show_expression("happy", "Mmm, pi!")
            elif value < 0:
                self.show_expression("sad", "Negative...")
            elif value > 9000:
                self.show_expression("surprised", "Over 9000!")
            elif value == 69 or value == 420:
                self.show_expression("wink", "Nice.")
            elif value > 1000000:
                self.show_expression("excited", "Huge number!")
            else:
                self.show_expression("happy")
        except (ValueError, TypeError):
            # Handle non-numeric results
            if "ERROR" in result:
                self.show_expression("error", "Oops!")
            else:
                self.show_expression("confused")
    
    def react_to_operation(self, operation):
        """
        React to specific calculator operations.
        
        Args:
            operation (str): The operation button pressed
        """
        if operation in OPERATION_REACTIONS:
            mood, message = OPERATION_REACTIONS[operation]
            self.show_expression(mood, message)
    
    def react_to_error(self, error_type):
        """
        React to calculator errors.
        
        Args:
            error_type (str): The type of error that occurred
        """
        if "division by zero" in error_type.lower():
            self.show_expression("error", "Can't divide by 0!")
        elif "syntax" in error_type.lower():
            self.show_expression("confused", "I don't understand!")
        else:
            self.show_expression("error", "Error!")
    
    def react_to_power_toggle(self, power_state):
        """
        React to calculator power being toggled.
        
        Args:
            power_state (bool): New power state
        """
        if power_state:
            self.show_expression("excited", "Hello!")
        else:
            self.show_expression("sad", "Goodbye!")