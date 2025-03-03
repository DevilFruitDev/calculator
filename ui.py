#!/usr/bin/env python3
"""
Game-Style Calculator - User Interface
A retro Game Boy-inspired calculator with animations and visual effects
"""
# Make sure this import is at the top and not commented out
from calculator_face import CalculatorFace
import tkinter as tk
from tkinter import font
import logging
import time
import random
import math  # Added for some effects


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
        import tkinter as tk
        
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
            text="^_^",  # Default happy face
            font=("Courier", 24, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["accent1"],
            padx=10
        )
        self.face_display.pack(side=tk.RIGHT, padx=10)
        
        # Create a text bubble for reactions
        self.bubble_frame = tk.Frame(
            self.face_frame,
            bg=self.colors["display_bg"],
            bd=2,
            relief=tk.RAISED
        )
        self.bubble_frame.pack(side=tk.RIGHT, padx=5)
        
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
    
    def show_expression(self, mood, message=""):
        """
        Show a facial expression and optional message.
        
        Args:
            mood (str): The mood to express (happy, sad, surprised, etc.)
            message (str): Optional message to display in bubble
        """
        # Dictionary of expressions for different moods
        expressions = {
            "happy": "^‿^",
            "very_happy": "ʘ‿ʘ",
            "sad": "°︵°",
            "surprised": "O_O",
            "confused": "⊙﹏⊙",
            "thinking": "•̀ᴗ•́",
            "excited": "✧◝(⁰▿⁰)◜✧",
            "error": "×_×",
            "cool": "⌐■_■",
            "wink": "^_~",
            "default": "^_^"
        }
        
        # Get the expression or use default
        face = expressions.get(mood, expressions["default"])
        
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
            "π": ("happy", "Pi time!")
        }
        
        if operation in reactions:
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

class CalculatorUI:
    """
    User interface for the video game style calculator.
    Handles all UI elements, animations, and user interaction.
    """
    
    def __init__(self, root, calculator):
        """
        Initialize the calculator UI.
        
        Args:
            root (tk.Tk): Tkinter root window
            calculator (Calculator): Calculator logic instance
        """
        self.root = root
        self.calculator = calculator
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing UI")
        
        # Configure window
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Initialize variables
        self.init_variables()
        
        # Create UI components
        self.build_ui()
        
        # Set up key bindings
        self.setup_key_bindings()
        
        # Start animations
        self.animate_scanline()
        
        # Start with powered off state
        self.root.after(500, self.power_on_animation)
    
    def init_variables(self):
        """Initialize variables and UI state."""
        # Color scheme - Game Boy Color inspired red and black palette
        self.colors = {
            "bg_dark": "#440000",        # Deep red (darker background)
            "bg_medium": "#880000",      # Medium red (cabinet color)
            "display_bg": "#000000",     # Black (screen background)
            "accent1": "#FF0000",        # Bright red (primary accent)
            "accent2": "#FF4444",        # Light red (secondary accent)
            "accent3": "#AA0000",        # Dark red (tertiary accent)
            "accent4": "#222222",        # Dark gray (contrast color)
            "text_bright": "#FFFFFF",    # White (bright text)
            "text_dim": "#AAAAAA",       # Light gray (dim text)
            "btn_shadow": "#220000"      # Very dark red (shadow)
        }
        
        # Display animation variables
        self.anim_chars = "01ABgH?!X$#@~"  # More varied animation characters
        self.is_animating = False
        self.scan_line_pos = 0
        
        # Easter Egg tracking
        self.konami_code = ["Up", "Up", "Down", "Down", "Left", "Right", "Left", "Right",]
        self.konami_index = 0
        self.secret_button_sequence = []
        self.easter_egg_activated = False
        
        # Secrets and easter eggs
        self.secret_codes = {
            "123456": self.activate_matrix_mode,
            "31337": self.activate_hacker_mode,
            "80085": self.activate_silly_mode,
            "42": self.activate_answer_mode
        }
        
        # Configure root
        self.root.configure(bg=self.colors["bg_dark"])
        self.root.title("Game Calc")  # Changed title to match Game Boy theme
        
        # Create fonts
        self.create_fonts()
        
        # Button storage
        self.buttons = []
    
    def create_fonts(self):
        """Create custom pixel-style fonts for Game Boy aesthetic."""
        try:
            # Try to use a more "pixel" style font if available
            self.display_font = font.Font(family="Press Start 2P", size=22, weight="bold")
            self.expr_font = font.Font(family="Press Start 2P", size=12)
            self.button_font = font.Font(family="Press Start 2P", size=12)
            self.small_font = font.Font(family="Press Start 2P", size=9)
            self.title_font = font.Font(family="Press Start 2P", size=18)
            self.is_pixel_font = True
        except:
            # Fall back to standard fonts if pixel font not available
            self.display_font = font.Font(family="Courier", size=28, weight="bold")
            self.expr_font = font.Font(family="Courier", size=14)
            self.button_font = font.Font(family="Courier", size=14, weight="bold")
            self.small_font = font.Font(family="Courier", size=10, weight="bold")
            self.title_font = font.Font(family="Courier", size=24, weight="bold")
            self.is_pixel_font = False
            
            # Log that we're using fallback fonts
            self.logger.info("Pixel fonts not available, using fallback fonts")
    
    #-------------------------------------------------------------------------
    # UI Construction Methods
    #-------------------------------------------------------------------------
    
    def build_ui(self):
        """Create all UI components in order."""
        self.create_arcade_cabinet()
        
        # Add this line right after create_arcade_cabinet()
        self.face = CalculatorFace(self.top_frame, self.colors)
        
        self.create_display()
        self.create_control_panel()
        self.create_button_panel()
        self.create_buttons()
    
    # Optional features - uncomment to enable
    # self.add_memory_buttons()
        
        # Optional features - uncomment to enable
        # self.add_memory_buttons()
    
    def create_arcade_cabinet(self):
        """Create the main cabinet-style frame."""
        # Main cabinet frame
        self.cabinet_frame = tk.Frame(
            self.root,
            bg=self.colors["bg_dark"],
            bd=0
        )
        self.cabinet_frame.place(x=0, y=0, width=500, height=650)
        
        # Decorative top
        self.top_frame = tk.Frame(
            self.cabinet_frame,
            bg=self.colors["bg_medium"],
            height=80,
            bd=0
        )
        self.top_frame.pack(fill=tk.X, padx=20, pady=(20,0))
        
        # Title label
        self.title_label = tk.Label(
            self.top_frame,
            text="CALC-BOY COLOR",
            font=self.title_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["accent1"]
        )
        self.title_label.pack(pady=20)
    
    def create_display(self):
        """Create the calculator display area."""
        # Screen bezel (monitor style)
        self.bezel_frame = tk.Frame(
            self.cabinet_frame,
            bg=self.colors["bg_medium"],
            bd=10,
            relief=tk.RAISED
        )
        self.bezel_frame.pack(fill=tk.X, padx=30, pady=10)
        
        # CRT screen effect
        self.screen_frame = tk.Frame(
            self.bezel_frame,
            bg=self.colors["display_bg"],
            bd=0
        )
        self.screen_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Expression display
        self.expr_display = tk.Label(
            self.screen_frame,
            font=self.expr_font,
            bg=self.colors["display_bg"],
            fg=self.colors["accent2"],
            anchor="e",
            text=""
        )
        self.expr_display.pack(fill=tk.X, padx=10, pady=(20,5))
        
        # Result display
        self.result_display = tk.Label(
            self.screen_frame,
            font=self.display_font,
            bg=self.colors["display_bg"],
            fg=self.colors["accent1"],
            anchor="e",
            text="0"
        )
        self.result_display.pack(fill=tk.X, padx=10, pady=(5,20))
        
        # Scanline effect (to be animated)
        self.scan_line = tk.Frame(
            self.screen_frame,
            height=4,
            bg=self.colors["accent1"],
            bd=0
        )
        self.scan_line.place(x=0, y=0, width=500)
    
    def create_control_panel(self):
        """Create the mode and control panel."""
        # Mode panel
        self.mode_frame = tk.Frame(
            self.cabinet_frame,
            bg=self.colors["bg_medium"],
            bd=5,
            relief=tk.RAISED
        )
        self.mode_frame.pack(fill=tk.X, padx=40, pady=5)
        
        # Mode label with pixel effect
        self.mode_label = tk.Label(
            self.mode_frame,
            text="MODE",
            font=self.small_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["accent2"]
        )
        self.mode_label.pack(side=tk.LEFT, padx=5)
        
        # DEG mode button
        self.deg_btn = tk.Button(
            self.mode_frame,
            text="DEG",
            font=self.small_font,
            bg=self.colors["accent3"],
            fg=self.colors["text_bright"],
            activebackground=self.colors["accent3"],
            activeforeground=self.colors["text_bright"],
            relief=tk.RAISED,
            bd=3,
            command=lambda: self.toggle_angle_mode("DEG")
        )
        self.deg_btn.pack(side=tk.LEFT, padx=5)
        
        # RAD mode button
        self.rad_btn = tk.Button(
            self.mode_frame,
            text="RAD",
            font=self.small_font,
            bg=self.colors["bg_dark"],
            fg=self.colors["text_dim"],
            activebackground=self.colors["accent3"],
            activeforeground=self.colors["text_bright"],
            relief=tk.RAISED,
            bd=3,
            command=lambda: self.toggle_angle_mode("RAD")
        )
        self.rad_btn.pack(side=tk.LEFT, padx=5)
        
        # POWER button (with glowing effect)
        self.power_btn = tk.Button(
            self.mode_frame,
            text="POWER",
            font=self.small_font,
            bg=self.colors["accent1"],
            fg=self.colors["text_bright"],
            activebackground=self.colors["accent1"],
            activeforeground=self.colors["text_bright"],
            relief=tk.RAISED,
            bd=1,
            command=self.toggle_power
        )
        self.power_btn.pack(side=tk.RIGHT, padx=10)
    
    def create_button_panel(self):
        """Create the main panel that will hold the calculator buttons."""
        # Main buttons panel designed like arcade controls
        self.buttons_panel = tk.Frame(
            self.cabinet_frame,
            bg=self.colors["bg_medium"],
            bd=1,
            relief=tk.RAISED
        )
        self.buttons_panel.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Configure grid for buttons
        self.buttons_frame = tk.Frame(
            self.buttons_panel,
            bg=self.colors["bg_dark"],
            bd=5,
            relief=tk.SUNKEN
        )
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)  # Increased padding
        
        # Create grid layout with more space between cells
        for i in range(5):
            self.buttons_frame.columnconfigure(i, weight=1, minsize=50)  # Add minsize
            self.buttons_frame.rowconfigure(i, weight=1, minsize=40)  # Add minsize
    
    def create_buttons(self):
        """Create calculator buttons with video game styling."""
        # Button definitions: [row, col, text, command, color, text_color]
        button_configs = self.get_button_configurations()
        
        # Create each button with arcade style
        for btn in button_configs:
            self.create_single_button(btn)
        
        # Special case for equals button
        self.create_equals_button()
    
    def get_button_configurations(self):
        """Return the configuration for all buttons."""
        return [
            # Row 0
            [0, 0, "C", self.clear, self.colors["accent1"], self.colors["text_bright"]],
            [0, 1, "AC", self.all_clear, self.colors["accent1"], self.colors["text_bright"]],
            [0, 2, "(", lambda: self.insert_text("("), self.colors["accent3"], self.colors["text_bright"]],
            [0, 3, ")", lambda: self.insert_text(")"), self.colors["accent3"], self.colors["text_bright"]],
            [0, 4, "←", self.backspace, self.colors["accent4"], self.colors["text_bright"]],
            
            # Row 1
            [1, 0, "π", lambda: self.insert_text("π"), self.colors["accent3"], self.colors["text_bright"]],
            [1, 1, "sin", lambda: self.insert_function("sin("), self.colors["accent3"], self.colors["text_bright"]],
            [1, 2, "cos", lambda: self.insert_function("cos("), self.colors["accent3"], self.colors["text_bright"]],
            [1, 3, "tan", lambda: self.insert_function("tan("), self.colors["accent3"], self.colors["text_bright"]],
            [1, 4, "^", lambda: self.insert_text("^"), self.colors["accent2"], self.colors["display_bg"]],
            
            # Row 2
            [2, 0, "7", lambda: self.insert_text("7"), self.colors["bg_medium"], self.colors["text_bright"]],
            [2, 1, "8", lambda: self.insert_text("8"), self.colors["bg_medium"], self.colors["text_bright"]],
            [2, 2, "9", lambda: self.insert_text("9"), self.colors["bg_medium"], self.colors["text_bright"]],
            [2, 3, "÷", lambda: self.insert_text("÷"), self.colors["accent2"], self.colors["display_bg"]],
            [2, 4, "√", lambda: self.insert_function("sqrt("), self.colors["accent3"], self.colors["text_bright"]],
            
            # Row 3
            [3, 0, "4", lambda: self.insert_text("4"), self.colors["bg_medium"], self.colors["text_bright"]],
            [3, 1, "5", lambda: self.insert_text("5"), self.colors["bg_medium"], self.colors["text_bright"]],
            [3, 2, "6", lambda: self.insert_text("6"), self.colors["bg_medium"], self.colors["text_bright"]],
            [3, 3, "×", lambda: self.insert_text("×"), self.colors["accent2"], self.colors["display_bg"]],
            [3, 4, "%", lambda: self.insert_text("%"), self.colors["accent3"], self.colors["text_bright"]],
            
            # Row 4
            [4, 0, "1", lambda: self.insert_text("1"), self.colors["bg_medium"], self.colors["text_bright"]],
            [4, 1, "2", lambda: self.insert_text("2"), self.colors["bg_medium"], self.colors["text_bright"]],
            [4, 2, "3", lambda: self.insert_text("3"), self.colors["bg_medium"], self.colors["text_bright"]],
            [4, 3, "-", lambda: self.insert_text("-"), self.colors["accent2"], self.colors["display_bg"]],
            
            # Row 5
            [5, 0, "0", lambda: self.insert_text("0"), self.colors["bg_medium"], self.colors["text_bright"]],
            [5, 2, ".", lambda: self.insert_text("."), self.colors["bg_medium"], self.colors["text_bright"]],
            [5, 3, "+", lambda: self.insert_text("+"), self.colors["accent2"], self.colors["display_bg"]],
        ]
    
    def create_single_button(self, btn_config):
        """Create a single button based on its configuration."""
        row, col, text, command, bg_color, fg_color = btn_config
        
        # Special case for the zero button
        if text == "0":
            columnspan = 2
            sticky = "nsew"
        else:
            columnspan = 1
            sticky = "nsew"
        
        # Create a frame for 3D effect
        btn_frame = tk.Frame(
            self.buttons_frame,
            bg=self.colors["btn_shadow"],
            bd=0,
            highlightthickness=0
        )
        btn_frame.grid(row=row, column=col, columnspan=columnspan, padx=5, pady=5, sticky=sticky)  # Increased padding
        
        # Create the button with pixel-art style - increase button font size
        button = tk.Button(
            btn_frame,
            text=text,
            font=font.Font(family=self.button_font.cget("family"), size=16, weight="bold"),  # Increased font size
            bg=bg_color,
            fg=fg_color,
            activebackground=fg_color,
            activeforeground=bg_color,
            relief=tk.RAISED,
            bd=3,  # Increased border width for larger 3D effect
            command=command
        )
        button.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)  # Slightly increased internal padding
        self.buttons.append(button)
    
    def create_equals_button(self):
        """Create the special equals button."""
        equals_frame = tk.Frame(
            self.buttons_frame,
            bg=self.colors["btn_shadow"],
            bd=0,
            highlightthickness=0
        )
        equals_frame.grid(row=4, column=4, rowspan=2, padx=8, pady=8, sticky="nsew")  # Increased padding
        
        equals_button = tk.Button(
            equals_frame,
            text="=",
            font=font.Font(family=self.title_font.cget("family"), size=26, weight="bold"),  # Increased font size
            bg=self.colors["accent1"],
            fg=self.colors["text_bright"],
            activebackground=self.colors["text_bright"],
            activeforeground=self.colors["accent1"],
            relief=tk.RAISED,
            bd=6,  # Increased border width
            command=self.calculate
        )
        equals_button.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)  # Slightly increased internal padding
        self.buttons.append(equals_button)
    
    #-------------------------------------------------------------------------
    # Animation and Visual Effects
    #-------------------------------------------------------------------------
    
    def power_on_animation(self):
        """Game Boy inspired power-on sequence."""
        self.is_animating = True
        
        # Enable all buttons
        for button in self.buttons:
            button.config(state=tk.NORMAL)
        
        # Game Boy boot sound effect would go here
        # self.play_special_sound("gameboy_boot.wav")
        
        # Classic Game Boy green screen flash
        self.screen_frame.config(bg="#AAFFAA") 
        self.result_display.config(fg="#000000")
        self.expr_display.config(fg="#000000")
        self.root.update()
        time.sleep(0.5)
        
        # Nintendo-style logo drop animation (simplified)
        self.result_display.config(text="GAME BOY")
        self.root.update()
        time.sleep(0.5)
        
        # Boot sequence on the display
        boot_text = [
            "GameCalc®",
            "LOADING...",
            "CALC OS v1.0",
            "READY."
        ]
        
        # Restore normal colors
        self.screen_frame.config(bg=self.colors["display_bg"])
        self.result_display.config(fg=self.colors["accent1"])
        self.expr_display.config(fg=self.colors["accent2"])
        
        for text in boot_text:
            self.result_display.config(text=text)
            self.root.update()
            time.sleep(0.4)
        
        # Random characters effect
        for _ in range(10):
            chars = "".join(random.choice(self.anim_chars) for _ in range(8))
            self.result_display.config(text=chars)
            self.root.update()
            time.sleep(0.05)
        
        # Clear and show ready state
        self.result_display.config(text="0")
        self.calculator.power_on = True
        self.is_animating = False
        
        # Pulse effect on the equals button
        self.pulse_button()
        
        # Sequence of button highlights
        self.sequence_highlight_buttons()
        
        # 1 in 20 chance to show a special greeting
        if random.randint(1, 20) == 1:
            self.root.after(1000, self.show_rare_greeting)
    
    def power_off_animation(self):
        """Animated power-down sequence."""
        self.is_animating = True
        
        # Flash display
        self.flash_display()
        
        # Show shutdown message
        self.result_display.config(text="SHUTTING DOWN")
        self.expr_display.config(text="")
        self.root.update()
        time.sleep(0.5)
        
        # Fade out effect
        for i in range(10):
            if i % 2 == 0:
                self.result_display.config(text="")
            else:
                self.result_display.config(text="SHUTTING DOWN")
            self.root.update()
            time.sleep(0.1)
        
        # New: Add spiral effect on buttons before turning off
        self.spiral_button_effect()
        
        # Black screen
        self.result_display.config(text="")
        self.expr_display.config(text="")
        
        # Disable all buttons
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        
        self.is_animating = False
    
    def pulse_button(self, button_idx=0):
        """Create a pulsing effect on buttons."""
        if not self.calculator.power_on:
            return
            
        # Reference to the equals button (last in the list)
        if not self.buttons:
            return
            
        # Get the button to pulse (default is the equals button)
        btn_to_pulse = self.buttons[-1] if button_idx == 0 else self.buttons[button_idx]
        
        # Store original color
        original_bg = btn_to_pulse.cget("background")
        original_fg = btn_to_pulse.cget("foreground")
        
        # Pulse effect (swap colors)
        btn_to_pulse.config(
            bg=original_fg,
            fg=original_bg
        )
        
        # Reset after delay
        self.root.after(100, lambda: btn_to_pulse.config(
            bg=original_bg,
            fg=original_fg
        ))
        
        # Continue pulsing if still powered on
        if self.calculator.power_on:
            self.root.after(2000, lambda: self.pulse_button(button_idx))
    
    def flash_display(self):
        """Create a flash effect on the display."""
        if self.is_animating:
            return
            
        # Store original colors
        original_bg = self.screen_frame.cget("background")
        original_fg = self.result_display.cget("foreground")
        
        # Flash effect
        self.screen_frame.config(bg=self.colors["accent1"])
        self.result_display.config(fg=self.colors["display_bg"])
        self.expr_display.config(fg=self.colors["display_bg"])
        
        # Reset after delay
        self.root.after(50, lambda: (
            self.screen_frame.config(bg=original_bg),
            self.result_display.config(fg=original_fg),
            self.expr_display.config(fg=self.colors["accent2"])
        ))
    
    def animate_scanline(self):
        """Animate a CRT-style scanline effect."""
        if not self.calculator.power_on and not self.is_animating:
            # Only update position every few calls when off
            self.scan_line.place_forget()
            self.root.after(100, self.animate_scanline)
            return
            
        # Update scanline position
        screen_height = self.screen_frame.winfo_height()
        if screen_height > 10:  # Ensure screen has been rendered
            self.scan_line_pos = (self.scan_line_pos + 4) % screen_height
            self.scan_line.place(x=0, y=self.scan_line_pos, width=self.screen_frame.winfo_width())
        
        # Continue animation
        self.root.after(50, self.animate_scanline)
    
    def show_result_animation(self, result):
        """Show result with animation effects."""
        # Flash the display
        self.flash_display()
        
        # Update the result display
        self.result_display.config(text=result)
        
        # Optional: add more animation here
        for _ in range(2):
            self.root.after(50, lambda: self.result_display.config(fg=self.colors["accent4"]))
            self.root.after(100, lambda: self.result_display.config(fg=self.colors["accent1"]))
        
        # New: Add number counting animation for small results
        try:
            result_value = float(result)
            if 0 <= result_value <= 100 and result_value.is_integer():
                self.count_up_animation(int(result_value))
        except (ValueError, TypeError):
            pass
    
    def show_error_animation(self, error):
        """Show error with animation effects in Game Boy style."""
        # Determine error type for custom messages
        error_type = self.categorize_error(error)
        
        # Play error sound effect (stub)
        # self.play_special_sound("error_beep.wav")
        
        # Flash the display in error color
        self.screen_frame.config(bg=self.colors["accent1"])
        self.result_display.config(fg=self.colors["display_bg"])
        self.expr_display.config(fg=self.colors["display_bg"])
        
        # Get custom error message based on error type
        error_message = self.get_error_message(error_type)
        
        # Show error message with game-like appearance
        self.result_display.config(text=error_message)
        if len(error) > 20:
            short_error = error[:17] + "..."
        else:
            short_error = error
        self.expr_display.config(text=short_error)
        
        # Game Boy style screen glitch effect
        self.glitch_screen_effect()
        
        # Retro game style blink effect
        for i in range(4):
            self.root.after(i*150, lambda: self.result_display.config(text=""))
            self.root.after(i*150+75, lambda: self.result_display.config(text=error_message))
        
        # Shake calculator window on error
        self.shake_window()
        
        # Pixel-drop effect (simulates screen breaking)
        self.pixel_drop_effect()
        
        # Reset after all animations complete
        total_delay = 1500
        self.root.after(total_delay, lambda: (
            self.screen_frame.config(bg=self.colors["display_bg"]),
            self.result_display.config(fg=self.colors["accent1"]),
            self.expr_display.config(fg=self.colors["accent2"]),
            self.result_display.config(text="0"),
            self.expr_display.config(text="")
        ))

    def categorize_error(self, error_text):
        """Categorize the error type based on the error message."""
        error_lower = error_text.lower()
        
        if "division by zero" in error_lower:
            return "divide_by_zero"
        elif "invalid syntax" in error_lower:
            return "syntax"
        elif "math domain error" in error_lower:
            return "domain"
        elif "overflow" in error_lower:
            return "overflow"
        elif "parentheses" in error_lower or "(" in error_lower or ")" in error_lower:
            return "parentheses"
        else:
            return "general"

    def get_error_message(self, error_type):
        """Get a game-style error message based on error type."""
        messages = {
            "divide_by_zero": "FATAL ERROR!",
            "syntax": "SYNTAX ERROR",
            "domain": "MATH ERROR",
            "overflow": "OVERFLOW",
            "parentheses": "PAREN ERROR",
            "general": "ERROR"
        }
        
        # Add some fun Game Boy style messages
        game_messages = {
            "divide_by_zero": ["FATAL ERROR!", "GAME OVER", "DIV BY ZERO", "INFINITY"],
            "syntax": ["SYNTAX ERROR", "BAD COMMAND", "INVALID CODE"],
            "domain": ["MATH ERROR", "IMPOSSIBLE", "OUT OF RANGE"],
            "overflow": ["OVERFLOW", "TOO BIG!", "NUMBER LIMIT"],
            "parentheses": ["PAREN ERROR", "MISSING )", "BRACKET MISMATCH"],
            "general": ["ERROR", "MALFUNCTION", "GAME OVER", "SYSTEM HALT"]
        }
        
        # Get a random message for this error type
        return random.choice(game_messages[error_type])

    def glitch_screen_effect(self):
        """Create a screen glitch effect like old Game Boy games."""
        original_bg = self.screen_frame.cget("background")
        
        # Random static effect colors
        glitch_colors = ["#FF0000", "#FFFFFF", "#000000", "#880000"]
        
        # Apply quick random color changes
        for i in range(5):
            color = random.choice(glitch_colors)
            self.root.after(i*50, lambda c=color: self.screen_frame.config(bg=c))
        
        # Restore original background
        self.root.after(250, lambda: self.screen_frame.config(bg=original_bg))

    def pixel_drop_effect(self):
        """Create an effect like pixels falling, simulating a broken screen."""
        # This simulates pixels falling by creating and animating small frames
        screen_width = self.screen_frame.winfo_width()
        screen_height = self.screen_frame.winfo_height()
        
        # Skip if screen is not properly sized yet
        if screen_width < 50 or screen_height < 50:
            return
        
        # Create 5-10 "falling pixels"
        num_pixels = random.randint(5, 10)
        
        for _ in range(num_pixels):
            # Random position and size
            pixel_width = random.randint(4, 12)
            pixel_height = random.randint(4, 8)
            pixel_x = random.randint(10, screen_width - pixel_width - 10)
            pixel_y = random.randint(10, 30)  # Start near top
            
            # Create a small frame for the "pixel"
            pixel = tk.Frame(
                self.screen_frame,
                width=pixel_width,
                height=pixel_height,
                bg=self.colors["accent1"]
            )
            pixel.place(x=pixel_x, y=pixel_y)
            
            # Animate the pixel falling
            fall_distance = screen_height - pixel_y - pixel_height - 10
            animation_steps = random.randint(8, 15)
            step_size = fall_distance / animation_steps
            
            for step in range(animation_steps):
                new_y = pixel_y + step * step_size
                delay = 100 + step * 30  # Accelerate as it falls
                self.root.after(delay, lambda p=pixel, ny=new_y: p.place(y=ny))
            
            # Remove the pixel at the end of animation
            self.root.after(100 + animation_steps * 30 + 100, lambda p=pixel: p.destroy())
    
    # New Animation Methods
    
    def sequence_highlight_buttons(self):
        """Create a sequence of button highlights during startup."""
        if not self.calculator.power_on or not self.buttons:
            return
            
        # Define delay between highlights
        delay = 50
        
        # Get all buttons
        for i, button in enumerate(self.buttons):
            # Store original colors
            original_bg = button.cget("background")
            original_fg = button.cget("foreground")
            
            # Schedule highlight
            self.root.after(i * delay, lambda btn=button, bg=original_bg, fg=original_fg: (
                btn.config(bg=self.colors["accent3"]),
                self.root.after(100, lambda: btn.config(bg=bg, fg=fg))
            ))
    
    def spiral_button_effect(self):
        """Create a spiral effect on buttons during shutdown."""
        if not self.buttons:
            return
        
        # Create spiral order of indices
        # This assumes buttons are in a grid layout
        num_buttons = len(self.buttons)
        spiral_indices = self.get_spiral_indices(num_buttons)
        
        # Apply spiral effect
        for i, idx in enumerate(spiral_indices):
            if idx < num_buttons:
                btn = self.buttons[idx]
                self.root.after(i * 50, lambda b=btn: b.config(bg=self.colors["accent1"]))
    
    def get_spiral_indices(self, num_buttons):
        """Generate spiral indices for buttons."""
        # Estimate grid dimensions (assumes rectangular grid)
        grid_size = int(math.sqrt(num_buttons))
        if grid_size * grid_size < num_buttons:
            grid_size += 1
            
        # Create empty 2D grid
        grid = [[-1 for _ in range(grid_size)] for _ in range(grid_size)]
        
        # Map 1D indices to 2D grid
        idx = 0
        for row in range(grid_size):
            for col in range(grid_size):
                if idx < num_buttons:
                    grid[row][col] = idx
                    idx += 1
        
        # Create spiral indices
        result = []
        top, bottom = 0, grid_size - 1
        left, right = 0, grid_size - 1
        
        while top <= bottom and left <= right:
            # Top row
            for col in range(left, right + 1):
                if grid[top][col] != -1:
                    result.append(grid[top][col])
            top += 1
            
            # Right column
            for row in range(top, bottom + 1):
                if grid[row][right] != -1:
                    result.append(grid[row][right])
            right -= 1
            
            # Bottom row
            if top <= bottom:
                for col in range(right, left - 1, -1):
                    if grid[bottom][col] != -1:
                        result.append(grid[bottom][col])
                bottom -= 1
            
            # Left column
            if left <= right:
                for row in range(bottom, top - 1, -1):
                    if grid[row][left] != -1:
                        result.append(grid[row][left])
                left += 1
                
        return result
    
    def count_up_animation(self, target_value):
        """Animate counting up to the result value."""
        if target_value <= 0 or target_value > 100:
            return
            
        # Store original value
        original_text = self.result_display.cget("text")
        
        # Determine speed of animation
        step = max(1, target_value // 20)
        delay = 1000 // target_value  # Faster for larger numbers
        
        # Animation function
        def animate_count(current=0):
            if current > target_value:
                # Restore final value
                self.result_display.config(text=original_text)
                return
                
            self.result_display.config(text=str(current))
            self.root.update()
            self.root.after(delay, lambda: animate_count(current + step))
        
        # Start animation after a short delay
        self.root.after(300, lambda: animate_count())
    
    def shake_window(self):
        """Create a shaking effect on the calculator window."""
        original_x = self.root.winfo_x()
        original_y = self.root.winfo_y()
        
        # Define shake pattern (offset, delay)
        shake_pattern = [
            (5, 0), (-10, 50), (8, 100), (-6, 150), 
            (4, 200), (-2, 250), (0, 300)
        ]
                # Apply shake
        for offset_x, delay in shake_pattern:
            self.root.after(
                delay, 
                lambda x=offset_x: self.root.geometry(f"+{original_x + x}+{original_y}")
            )
        
        # Reset position
        self.root.after(350, lambda: self.root.geometry(f"+{original_x}+{original_y}"))
        
    def show_rare_greeting(self):
        """Rarely shown special greeting - easter egg."""
        greetings = [
            "HI PLAYER 1",
            "INSERT COIN",
            "READY PLAYER 1",
            "PRESS START",
            "SECRET MODE?"
        ]
        
        greeting = random.choice(greetings)
        original_text = self.result_display.cget("text")
        
        # Show greeting with typing effect
        self.create_typing_effect(greeting, self.result_display, delay=100)
        
        # Restore original display after a delay
        self.root.after(2000, lambda: self.result_display.config(text=original_text))
    
    #-------------------------------------------------------------------------
    # Easter Egg Features and Secret Animations
    #-------------------------------------------------------------------------

    def check_konami_code(self, key):
        """Check if the Konami code is being entered."""
        expected_key = self.konami_code[self.konami_index]
        if key == expected_key:
            self.konami_index += 1
            if self.konami_index == len(self.konami_code):
                self.activate_cheat_mode()
                self.konami_index = 0
                return True
        else:
            self.konami_index = 0
        return False

    def activate_cheat_mode(self):
        """Activate cheat mode when Konami code is entered correctly."""
        # Flash all buttons in sequence
        self.button_wave_animation()
        
        # Play 8-bit style sound (if sound was implemented)
        # self.play_special_sound("powerup.wav")
        
        # Show secret message
        original_text = self.result_display.cget("text")
        self.result_display.config(text="CHEAT MODE ON")
        self.expr_display.config(text="30 LIVES")
        
        # Game Boy-style notification
        self.screen_frame.config(bg="#AAFFAA")  # Classic Game Boy green
        self.root.update()
        time.sleep(1)
        
        # Restore display
        self.screen_frame.config(bg=self.colors["display_bg"])
        self.result_display.config(text=original_text)
        self.expr_display.config(text="")
        
        # Set easter egg flag
        self.easter_egg_activated = True

    def activate_matrix_mode(self):
        """Easter egg: Matrix-style display mode."""
        self.create_matrix_effect(duration=5000)
        
        # Change color scheme temporarily
        original_colors = self.colors.copy()
        self.colors["accent1"] = "#00FF00"  # Matrix green
        self.colors["accent2"] = "#00AA00"  # Darker green
        self.colors["accent3"] = "#003300"  # Very dark green
        
        # Revert colors after 10 seconds
        self.root.after(10000, lambda: self.restore_colors(original_colors))

    def activate_hacker_mode(self):
        """Easter egg: Hacker mode with terminal-like appearance."""
        # Flash screen
        self.flash_display()
        
        # Show "hacking" message
        self.result_display.config(text="ACCESS GRANTED")
        self.expr_display.config(text="HACKING THE MAINFRAME...")
        
        # Rapid typing effect with random characters
        def type_random_chars(count=0):
            if count > 20:
                self.result_display.config(text="0")
                self.expr_display.config(text="")
                return
                
            chars = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(15))
            self.expr_display.config(text=f"HACKING: {chars}")
            self.root.after(100, lambda: type_random_chars(count + 1))
        
        # Start the typing effect
        self.root.after(1000, type_random_chars)

    def activate_silly_mode(self):
        """Easter egg: Silly calculator mode with rainbow effects."""
        # Play a silly sound
        # self.play_special_sound("laugh.wav")
        
        # Show silly message
        self.result_display.config(text="VERY MATURE")
        
        # Rainbow effect
        self.rainbow_display(cycles=3, speed=100)
        
        # After rainbow, restore normal display
        self.root.after(2000, lambda: self.result_display.config(text="0"))

    def activate_answer_mode(self):
        """Easter egg: The answer to life, the universe, and everything."""
        # Deep thought animation
        self.result_display.config(text="THINKING...")
        self.expr_display.config(text="DEEP THOUGHT")
        
        # Countdown timer
        for i in range(5, 0, -1):
            self.root.after(i * 1000 - 5000, lambda t=i: self.result_display.config(text=f"T-MINUS {t}"))
        
        # Final answer reveal
        self.root.after(5000, lambda: (
            self.result_display.config(text="42"),
            self.expr_display.config(text="THE ANSWER IS")
        ))
        
        # Flash the display dramatically
        self.root.after(5100, self.flash_display)
        self.root.after(5300, self.flash_display)
        self.root.after(5500, self.flash_display)

    def restore_colors(self, original_colors):
        """Restore original color scheme after an easter egg."""
        self.colors = original_colors
        
        # Update button colors
        for button in self.buttons:
            # Only update if it's a normal button
            if button.cget("text") not in ["=", "C", "AC"]:
                button.config(bg=self.colors["bg_medium"])
        
        # Update other UI elements
        self.screen_frame.config(bg=self.colors["display_bg"])
        self.result_display.config(fg=self.colors["accent1"])
        self.expr_display.config(fg=self.colors["accent2"])

    def check_secret_code(self):
        """Check if a secret code has been entered in the expression."""
        expression = self.calculator.current_expression
        
        # Check for any secret codes
        for code, action in self.secret_codes.items():
            if code in expression:
                # Clear the expression to hide the code
                self.calculator.current_expression = ""
                self.expr_display.config(text="")
                
                # Activate the corresponding easter egg
                action()
                return True
        
        return False
        
    def create_typing_effect(self, text, display_widget, delay=50):
        """Create a typing effect for text."""
        original_text = display_widget.cget("text")
        
        def type_char(idx=0):
            if idx <= len(text):
                display_widget.config(text=text[:idx])
                self.root.update()
                self.root.after(delay, lambda: type_char(idx + 1))
            else:
                # Animation complete
                pass
                
        # Start typing animation
        type_char()
        
        # Return original text for reference
        return original_text
    
    def create_matrix_effect(self, duration=2000):
        """Create a Matrix-style rain effect on the display."""
        if not self.calculator.power_on:
            return
            
        self.is_animating = True
        original_text = self.result_display.cget("text")
        original_expr = self.expr_display.cget("text")
        
        # Characters for matrix effect
        matrix_chars = "01"
        screen_width = 10  # Approximate character width
        
        def update_matrix(remaining_time):
            if remaining_time <= 0:
                # Restore original display
                self.result_display.config(text=original_text)
                self.expr_display.config(text=original_expr)
                self.is_animating = False
                return
                
            # Generate random matrix characters
            result_text = "".join(random.choice(matrix_chars) for _ in range(screen_width))
            expr_text = "".join(random.choice(matrix_chars) for _ in range(screen_width))
            
            # Update displays
            self.result_display.config(text=result_text)
            self.expr_display.config(text=expr_text)
            
            # Continue animation
            self.root.after(100, lambda: update_matrix(remaining_time - 100))
            
        # Start matrix animation
        update_matrix(duration)
        
    def rainbow_display(self, cycles=2, speed=50):
        """Create a rainbow cycling effect on the display."""
        if not self.calculator.power_on:
            return
            
        # Define rainbow colors (in hex)
        rainbow_colors = [
            "#FF0000", "#FF7F00", "#FFFF00", "#00FF00", 
            "#0000FF", "#4B0082", "#8B00FF"
        ]
        
        # Store original colors
        original_bg = self.screen_frame.cget("background")
        original_fg = self.result_display.cget("foreground")
        original_expr_fg = self.expr_display.cget("foreground")
        
        # Calculate total steps
        total_steps = cycles * len(rainbow_colors)
        
        def cycle_color(step=0):
            if step >= total_steps:
                # Restore original colors
                self.screen_frame.config(bg=original_bg)
                self.result_display.config(fg=original_fg)
                self.expr_display.config(fg=original_expr_fg)
                return
                
            # Get current color
            color_idx = step % len(rainbow_colors)
            current_color = rainbow_colors[color_idx]
            
            # Update colors
            self.screen_frame.config(bg=current_color)
            # Use contrasting color for text
            text_color = "#FFFFFF" if color_idx > 2 else "#000000"
            self.result_display.config(fg=text_color)
            self.expr_display.config(fg=text_color)
            
            # Continue cycle
            self.root.after(speed, lambda: cycle_color(step + 1))
            
        # Start color cycling
        cycle_color()
    
    def button_wave_animation(self):
        """Create a wave effect across calculator buttons."""
        if not self.calculator.power_on or not self.buttons:
            return
            
        # Estimate grid dimensions
        num_buttons = len(self.buttons)
        cols = int(math.sqrt(num_buttons))
        
        # Create wave pattern based on button position
        for i, button in enumerate(self.buttons):
            row = i // cols
            col = i % cols
            
            # Calculate delay based on position (creates wave effect)
            delay = (row + col) * 50
            
            # Store original colors
            original_bg = button.cget("background")
            original_fg = button.cget("foreground")
            
            # Schedule highlight with delay
            self.root.after(delay, lambda btn=button, bg=original_bg, fg=original_fg: (
                btn.config(bg=self.colors["accent2"]),
                self.root.after(100, lambda: btn.config(bg=bg, fg=fg))
            ))
    
    #-------------------------------------------------------------------------
    # Button Actions and Event Handlers
    #-------------------------------------------------------------------------
    
    def toggle_angle_mode(self, mode):
        """Toggle between DEG and RAD with visual feedback."""
        if not self.calculator.power_on:
            return
            
        self.calculator.set_angle_mode(mode)
        
        if mode == "DEG":
            self.deg_btn.config(
                bg=self.colors["accent3"],
                fg=self.colors["text_bright"]
            )
            self.rad_btn.config(
                bg=self.colors["bg_dark"],
                fg=self.colors["text_dim"]
            )
        else:
            self.deg_btn.config(
                bg=self.colors["bg_dark"],
                fg=self.colors["text_dim"]
            )
            self.rad_btn.config(
                bg=self.colors["accent3"],
                fg=self.colors["text_bright"]
            )
            
        # Flash the display briefly for feedback
        self.flash_display()
    
    def toggle_power(self):
        """Toggle power with animation effects."""
        new_power_state = self.calculator.toggle_power()
        
        # Add this line to react to power state change
        self.face.react_to_power_toggle(new_power_state)
        
        if new_power_state:
            self.power_on_animation()
        else:
            self.power_off_animation()
    
    def insert_text(self, text):
        """Insert text into the expression and update display."""
        if not self.calculator.power_on:
            return
            
        # Update calculator state
        self.calculator.insert_text(text)
        
        # Update display
        self.expr_display.config(text=self.calculator.current_expression)
        
        # React to operation buttons
        if text in ["+", "-", "×", "÷", "^", "%"]:
            self.face.react_to_operation(text)
        
        # Check for secret codes
        self.check_secret_code()
        
        # Play sound effect (stub)
        self.play_click_sound()
    
    def insert_function(self, func):
        """Insert a function into the expression and update display."""
        if not self.calculator.power_on:
            return
            
        # Update calculator state
        self.calculator.insert_function(func)
        
        # Update display
        self.expr_display.config(text=self.calculator.current_expression)
        
        # Play sound effect (stub)
        self.play_click_sound()
    
    def clear(self):
        """Clear the current expression."""
        if not self.calculator.power_on:
            return
            
        # Update calculator state
        self.calculator.clear()
        
        # Update display
        self.expr_display.config(text="")
        
        # Flash display for feedback
        self.flash_display()
    
    def all_clear(self):
        """Clear everything (AC button)."""
        if not self.calculator.power_on:
            return
            
        # Update calculator state
        expr, result = self.calculator.all_clear()
        
        # Update display
        self.expr_display.config(text=expr)
        self.result_display.config(text=result)
        
        # Flash display for feedback
        self.flash_display()
    
    def backspace(self):
        """Remove the last character (backspace)."""
        if not self.calculator.power_on:
            return
            
        # Update calculator state
        self.calculator.backspace()
        
        # Update display
        self.expr_display.config(text=self.calculator.current_expression)
        
        # Play sound effect (stub)
        self.play_click_sound()
    
    def calculate(self):
        """Calculate the result of the expression."""
        if not self.calculator.power_on:
            return
            
        # Flash equals button
        self.pulse_button(len(self.buttons) - 1)
        
        # Calculate expression
        success, result, error = self.calculator.calculate()
        
        if success:
            # Show result with animation
            self.show_result_animation(result)
            # Add this line to show face reaction
            self.face.react_to_calculation(result)
        else:
            # Show error
            self.show_error_animation(error)
            # Add this line for error reaction
            self.face.react_to_error(error)
    
    def handle_key(self, key):
        """Handle keyboard input."""
        if not self.calculator.power_on:
            return
            
        # Check for Konami code special keys first
        if self.check_konami_code(key):
            return
            
        # Flash the corresponding button
        for i, button in enumerate(self.buttons):
            if button.cget("text") == key:
                self.pulse_button(i)
                break
        
        # Update the calculator state
        self.insert_text(key)
    
    def setup_key_bindings(self):
        """Set up keyboard shortcuts."""
        # Number keys
        for i in range(10):
            self.root.bind(str(i), lambda e, digit=i: self.handle_key(str(digit)))
        
        # Operation keys
        self.root.bind("+", lambda e: self.handle_key("+"))
        self.root.bind("-", lambda e: self.handle_key("-"))
        self.root.bind("*", lambda e: self.handle_key("×"))
        self.root.bind("/", lambda e: self.handle_key("÷"))
        self.root.bind("^", lambda e: self.handle_key("^"))
        self.root.bind("%", lambda e: self.handle_key("%"))
        self.root.bind(".", lambda e: self.handle_key("."))
        
        # Parentheses
        self.root.bind("(", lambda e: self.handle_key("("))
        self.root.bind(")", lambda e: self.handle_key(")"))
        
        # Control keys
        self.root.bind("<Return>", lambda e: self.calculate())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<Escape>", lambda e: self.all_clear())
        self.root.bind("<Delete>", lambda e: self.clear())
        
        # Function keys
        self.root.bind("<F1>", lambda e: self.toggle_power())
        self.root.bind("<F2>", lambda e: self.toggle_angle_mode("DEG"))
        self.root.bind("<F3>", lambda e: self.toggle_angle_mode("RAD"))
        
        # Konami code keys
        self.root.bind("<Up>", lambda e: self.handle_key("Up"))
        self.root.bind("<Down>", lambda e: self.handle_key("Down"))
        self.root.bind("<Left>", lambda e: self.handle_key("Left"))
        self.root.bind("<Right>", lambda e: self.handle_key("Right"))
        self.root.bind("a", lambda e: self.handle_key("a"))
        self.root.bind("b", lambda e: self.handle_key("b"))
    
    #-------------------------------------------------------------------------
    # Sound Effects
    #-------------------------------------------------------------------------
    
    def play_click_sound(self):
        """Play a click sound effect (stub)."""
        # This is a stub for sound effects
        # In a real implementation, you might use pygame.mixer or another library
        pass
    
    #-------------------------------------------------------------------------
    # Optional Additional Features
    #-------------------------------------------------------------------------
    
    def add_memory_buttons(self):
        """Add memory-related buttons to the interface."""
        # Create a memory button panel
        memory_frame = tk.Frame(
            self.buttons_panel,
            bg=self.colors["bg_dark"],
            bd=0
        )
        memory_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Memory button definitions: [text, command, color]
        memory_buttons = [
            ["MC", self.memory_clear, self.colors["bg_medium"]],
            ["MR", self.memory_recall, self.colors["bg_medium"]],
            ["M+", self.memory_add, self.colors["bg_medium"]],
            ["M-", self.memory_subtract, self.colors["bg_medium"]]
        ]
        
        # Create each memory button
        for btn_def in memory_buttons:
            text, command, color = btn_def
            btn = tk.Button(
                memory_frame,
                text=text,
                font=self.small_font,
                bg=color,
                fg=self.colors["accent2"],
                activebackground=self.colors["accent2"],
                activeforeground=color,
                relief=tk.RAISED,
                bd=3,
                command=command
            )
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
            self.buttons.append(btn)
    
    def memory_clear(self):
        """Clear memory (MC button)."""
        if not self.calculator.power_on:
            return
            
        self.calculator.memory_clear()
        self.flash_display()
    
    def memory_recall(self):
        """Recall memory value (MR button)."""
        if not self.calculator.power_on:
            return
            
        expr = self.calculator.memory_recall()
        self.expr_display.config(text=expr)
    
    def memory_add(self):
        """Add to memory (M+ button)."""
        if not self.calculator.power_on:
            return
            
        self.calculator.memory_add()
        self.flash_display()
    
    def memory_subtract(self):
        """Subtract from memory (M- button)."""
        if not self.calculator.power_on:
            return
            
        self.calculator.memory_subtract()
        self.flash_display()
    
    def add_history_feature(self):
        """Add calculation history feature."""
        # Create history panel
        history_frame = tk.Frame(
            self.cabinet_frame,
            bg=self.colors["bg_medium"],
            bd=5,
            relief=tk.RAISED
        )
        history_frame.pack(fill=tk.X, padx=40, pady=5, before=self.buttons_panel)
        
        # History label
        history_label = tk.Label(
            history_frame,
            text="HISTORY",
            font=self.small_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["accent2"]
        )
        history_label.pack(side=tk.LEFT, padx=5)
        
        # History display (could be a listbox or text widget)
        self.history_display = tk.Listbox(
            history_frame,
            font=self.small_font,
            bg=self.colors["bg_dark"],
            fg=self.colors["text_bright"],
            selectbackground=self.colors["accent1"],
            height=3
        )
        self.history_display.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        # Bind event to recall history items
        self.history_display.bind("<Double-Button-1>", self.recall_history_item)
    
    def add_history_item(self, expression, result):
        """Add an item to the calculation history."""
        if hasattr(self, 'history_display'):
            entry = f"{expression} = {result}"
            self.history_display.insert(0, entry)
            # Keep only the last 10 entries
            if self.history_display.size() > 10:
                self.history_display.delete(10)
    
    def recall_history_item(self, event):
        """Recall a history item when clicked."""
        if not self.calculator.power_on:
            return
            
        # Get selected history item
        selection = self.history_display.curselection()
        if not selection:
            return
            
        item = self.history_display.get(selection[0])
        # Extract expression part (before the = sign)
        if "=" in item:
            expr = item.split("=")[0].strip()
            # Set as current expression
            self.calculator.current_expression = expr
            self.expr_display.config(text=expr)
            
            # Provide visual feedback
            self.flash_display()
