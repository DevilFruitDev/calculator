#!/usr/bin/env python3
"""
Game-Style Calculator - Face Component
A reactive face that gives personality to the calculator
"""

import tkinter as tk
import random

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
        self.face_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        # Create the face display label
        self.face_display = tk.Label(
            self.face_frame,
            text="^_^",  # Default happy face
            font=("Courier", 24, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["accent1"],
            padx=10
        )
        self.face_display.pack(padx=10)
        
        # Create a text bubble for reactions
        self.bubble_frame = tk.Frame(
            self.face_frame,
            bg=self.colors["display_bg"],
            bd=2,
            relief=tk.RAISED
        )
        self.bubble_frame.pack(pady=5)
        
        self.bubble_text = tk.Label(
            self.bubble_frame,
            text="Hello!",
            font=("Courier", 10),
            bg=self.colors["display_bg"],
            fg=self.colors["accent2"],
            padx=5,
            pady=2
        )
        self.bubble_text.pack()
        
        # Initialize with welcome expression
        self.show_expression("happy", "Ready to calculate!")
        
        # After a delay, hide the speech bubble
        self.parent.after(3000, self.hide_bubble)
        
        # Store consecutive operations counter
        self.consecutive_ops = {}
        self.last_op = None
    
    def show_expression(self, mood, message=""):
        """
        Show a facial expression and optional message.
        
        Args:
            mood (str): The mood to express (happy, sad, surprised, etc.)
            message (str): Optional message to display in bubble
        """
        # Dictionary of expressions for different moods
        expressions = {
            "happy": ["^‿^", "^_^", "◕‿◕"],
            "very_happy": ["ʘ‿ʘ", "≧◡≦", "◠‿◠"],
            "sad": ["°︵°", "◡﹏◡", "ಥ︵ಥ"],
            "surprised": ["O_O", "⊙.⊙", "Σ(°□°)"],
            "confused": ["⊙﹏⊙", "⊙_⊙", "ఠ_ఠ"],
            "thinking": ["•̀ᴗ•́", "ﾟ­_•", "¬_¬"],
            "excited": ["✧◝(⁰▿⁰)◜✧", "♥‿♥", "◕ ◡ ◕"],
            "error": ["×_×", "✖_✖", "☉_☉"],
            "cool": ["⌐■_■", "😎", "ლ(▀̿̿Ĺ̯̿̿▀̿ლ)"],
            "wink": ["^_~", ";‿◕", ";)"],
            "default": ["^_^", "◕‿◕"]
        }
        
        # Get the expression or use default - randomly select from options
        face_options = expressions.get(mood, expressions["default"])
        face = random.choice(face_options)
        
        # Update the face display
        self.face_display.config(text=face)
        
        # If there's a message, show the bubble
        if message:
            self.bubble_text.config(text=message)
            self.bubble_frame.pack(pady=5)
            
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
            elif value == 80085 or value == 8008:
                self.show_expression("wink", "Very mature...")
            elif value == 666:
                self.show_expression("cool", "Devilish!")
            elif value == 1337:
                self.show_expression("cool", "Leet!")
            elif value > 1000000:
                self.show_expression("excited", "Huge number!")
            elif value.is_integer():
                self.show_expression("happy")
            else:
                # Look for repeating decimals
                result_str = str(value)
                if len(set(result_str[-3:])) == 1:  # Repeating last 3 digits
                    self.show_expression("surprised", "Pattern!")
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
        # Track consecutive use of the same operation
        if operation == self.last_op:
            self.consecutive_ops[operation] = self.consecutive_ops.get(operation, 1) + 1
        else:
            self.consecutive_ops[operation] = 1
        
        self.last_op = operation
        
        # Base reactions
        reactions = {
            "+": ("happy", "Adding!"),
            "-": ("thinking", "Subtracting..."),
            "×": ("excited", "Multiplying!"),
            "÷": ("thinking", "Dividing..."),
            "=": ("very_happy", "Ta-da!"),
            "C": ("sad", "Clearing..."),
            "AC": ("surprised", "All gone!"),
            "^": ("excited", "To the power!"),
            "√": ("cool", "Finding roots!"),
            "%": ("thinking", "Percent!"),
            "sin": ("thinking", "Sine wave~"),
            "cos": ("thinking", "Cosine!"),
            "tan": ("thinking", "Tangent!"),
            "π": ("happy", "Pi time!"),
            "←": ("thinking", "Backspace!")
        }
        
        # Special reactions for consecutive operations
        if operation in self.consecutive_ops and self.consecutive_ops[operation] > 2:
            if operation == "+":
                self.show_expression("excited", "Adding frenzy!")
            elif operation == "×":
                self.show_expression("excited", "Multiply mania!")
            elif operation == "-":
                self.show_expression("confused", "Subtracting a lot?")
            elif operation == "÷":
                self.show_expression("surprised", "Division spree!")
            elif operation == "=":
                self.show_expression("confused", "Stop pressing =!")
        elif operation in reactions:
            mood, message = reactions[operation]
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
        elif "overflow" in error_type.lower():
            self.show_expression("surprised", "Too big!")
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
            
    def random_idle_reaction(self):
        """Generate a random idle reaction occasionally."""
        idle_reactions = [
            ("thinking", "Bored..."),
            ("happy", "Need help?"),
            ("wink", "Try pi!"),
            ("cool", "Math is fun!"),
            ("confused", "Any questions?")
        ]
        
        reaction = random.choice(idle_reactions)
        self.show_expression(reaction[0], reaction[1])