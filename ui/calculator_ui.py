"""
Game-Style Calculator - Main UI Controller
Coordinates all calculator UI components and manages modes
"""

import tkinter as tk
from tkinter import font
import logging
import time
import random

# Import UI components
from .components.calculator_face import CalculatorFace

# Import style definitions
from utils.styles import (
    ARCADE_COLORS, BASIC_COLORS, FONTS, 
    BUTTON_CONFIGS, ANIMATION
)

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
        # Set current color scheme (starts with arcade mode)
        self.colors = ARCADE_COLORS
        
        # Display animation variables
        self.anim_chars = "01ABgH?!X$#@~"  # More varied animation characters
        self.is_animating = False
        self.scan_line_pos = 0
        
        # Easter Egg tracking
        self.konami_code = ["Up", "Up", "Down", "Down", "Left", "Right", "Left", "Right"]
        self.konami_index = 0
        self.secret_button_sequence = []
        self.easter_egg_activated = False
        
        # Configure root
        self.root.configure(bg=self.colors["bg_dark"])
        self.root.title("Game Calc")  # Changed title to match Game Boy theme
        
        # Create fonts
        self.create_fonts()
        
        # Button storage
        self.buttons = []
        
        # Initialize arcade mode
        self.arcade_mode = True
        
    def create_fonts(self):
        """Create custom pixel-style fonts for Game Boy aesthetic."""
        try:
            # Try to use pixel style fonts
            self.display_font = font.Font(**FONTS["display"])
            self.expr_font = font.Font(**FONTS["expression"])
            self.button_font = font.Font(**FONTS["button"])
            self.small_font = font.Font(**FONTS["small"])
            self.title_font = font.Font(**FONTS["title"])
            self.is_pixel_font = True
        except:
            # Fall back to standard fonts if pixel font not available
            self.display_font = font.Font(**FONTS["fallback_display"])
            self.expr_font = font.Font(**FONTS["fallback_expression"])
            self.button_font = font.Font(**FONTS["fallback_button"])
            self.small_font = font.Font(**FONTS["fallback_small"])
            self.title_font = font.Font(**FONTS["fallback_title"])
            self.is_pixel_font = False
            
            # Log that we're using fallback fonts
            self.logger.info("Pixel fonts not available, using fallback fonts")
    
    #-------------------------------------------------------------------------
    # UI Construction Methods
    #-------------------------------------------------------------------------
    
    def build_ui(self):
        """Create all UI components in order."""
        self.create_arcade_cabinet()
        self.face = CalculatorFace(self.top_frame, self.colors)
        self.create_display()
        self.create_control_panel()
        self.create_button_panel()
        self.create_buttons()
        
        # Optional features
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
        self.title_label.pack(pady=(10, 5))  # Reduced bottom padding
        
        # Create status bar frame - NEW ADDITION
        self.status_frame = tk.Frame(
            self.top_frame,
            bg=self.colors["bg_medium"],
        )
        self.status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Battery indicator - NEW ADDITION
        self.battery_frame = tk.Frame(self.status_frame, bg=self.colors["bg_dark"], bd=1)
        self.battery_frame.pack(side=tk.RIGHT, padx=5)
        self.battery_canvas = tk.Canvas(self.battery_frame, width=30, height=15, 
                                    bg=self.colors["bg_dark"], highlightthickness=0)
        self.battery_canvas.pack()
        # Draw battery
        self.battery_canvas.create_rectangle(2, 4, 23, 12, outline=self.colors["accent1"])
        self.battery_canvas.create_rectangle(23, 6, 26, 10, fill=self.colors["accent1"], outline=self.colors["accent1"])
        self.battery_canvas.create_rectangle(4, 6, 20, 10, fill=self.colors["accent1"])
        
        # Add pixel art calculator icon - NEW ADDITION
        self.calc_icon = tk.Canvas(self.status_frame, width=16, height=16, 
                                bg=self.colors["bg_medium"], highlightthickness=0)
        self.calc_icon.pack(side=tk.LEFT, padx=5)
        # Draw pixel calculator
        self.calc_icon.create_rectangle(2, 2, 14, 14, outline=self.colors["accent1"])
        self.calc_icon.create_rectangle(4, 4, 12, 7, fill=self.colors["accent1"])
        
        # Add memory indicator (like Game Boy save icon) - NEW ADDITION
        self.memory_label = tk.Label(
            self.status_frame,
            text="MEM",
            font=self.small_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["accent2"]
        )
        self.memory_label.pack(side=tk.LEFT, padx=10)
        
        # Score-like display that shows calculations count - NEW ADDITION
        self.calc_count = 0
        self.score_label = tk.Label(
            self.status_frame,
            text="CALCS: 0",
            font=self.small_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["accent1"]
        )
        self.score_label.pack(side=tk.RIGHT, padx=10)

        # Game Boy-style "ridges" on the sides
        left_ridge = tk.Frame(self.cabinet_frame, bg="#550000", width=8, bd=0)
        left_ridge.place(x=5, y=85, height=480)
        right_ridge = tk.Frame(self.cabinet_frame, bg="#550000", width=8, bd=0)
        right_ridge.place(x=487, y=85, height=480)

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
        self.mode_frame.config(relief=tk.GROOVE, bd=2)
        self.mode_frame.pack(fill=tk.X, padx=35, pady=8)
        
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
        
        # Arcade/Basic mode toggle button
        self.mode_switch_btn = tk.Button(
            self.mode_frame,
            text="ARCADE MODE",
            font=self.small_font,
            bg=self.colors["accent3"],
            fg=self.colors["text_bright"],
            activebackground=self.colors["accent3"],
            activeforeground=self.colors["text_bright"],
            relief=tk.RAISED,
            bd=3,
            command=lambda: self.toggle_calculator_mode()
        )
        self.mode_switch_btn.pack(side=tk.LEFT, padx=10)
        
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
        
    # Include critical methods needed for basic functionality
    # (We'll move more to component files as we go)
    
    def create_button_panel(self):
        """Create the main panel that will hold the calculator buttons."""
        # Just add a placeholder implementation for now
        # We'll move this to button_panel.py later
        
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
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Create grid layout with more space between cells
        for i in range(5):
            self.buttons_frame.columnconfigure(i, weight=1, minsize=40)
            self.buttons_frame.rowconfigure(i, weight=1, minsize=35)
            
    def create_buttons(self):
        """Create calculator buttons with video game styling."""
        # Just add a placeholder implementation for now
        # We'll move this to button_panel.py later
        
        for btn_config in BUTTON_CONFIGS:
            self.create_single_button(btn_config)
        
        # Special case for equals button
        self.create_equals_button()
        
    def create_single_button(self, btn_config):
        """Create a single button based on its configuration."""
        # Placeholder implementation - will be moved to button_panel.py
        row, col, text, command_str, color_key, text_color_key = btn_config
        
        # Parse the command
        if ":" in command_str:
            method_name, arg = command_str.split(":")
            command = lambda arg=arg, method_name=method_name: getattr(self, method_name)(arg)
        else:
            command = getattr(self, command_str)
        
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
        btn_frame.grid(row=row, column=col, columnspan=columnspan, padx=5, pady=5, sticky=sticky)
        
        # Create the button with pixel-art style
        button = tk.Button(
            btn_frame,
            text=text,
            font=font.Font(family=self.button_font.cget("family"), size=10, weight="bold"),
            bg=self.colors[color_key],
            fg=self.colors[text_color_key],
            activebackground=self.colors[text_color_key],
            activeforeground=self.colors[color_key],
            relief=tk.RAISED,
            bd=2,
            command=command
        )
        button.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.buttons.append(button)
    
    def create_equals_button(self):
        """Create the special equals button."""
        equals_frame = tk.Frame(
            self.buttons_frame,
            bg=self.colors["btn_shadow"],
            bd=0,
            highlightthickness=0
        )
        equals_frame.grid(row=4, column=4, rowspan=2, padx=8, pady=8, sticky="nsew")
        
        equals_button = tk.Button(
            equals_frame,
            text="=",
            font=font.Font(family=self.title_font.cget("family"), size=26, weight="bold"),
            bg=self.colors["accent1"],
            fg=self.colors["text_bright"],
            activebackground=self.colors["text_bright"],
            activeforeground=self.colors["accent1"],
            relief=tk.RAISED,
            bd=6,
            command=self.calculate
        )
        equals_button.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        self.buttons.append(equals_button)
    
    #-------------------------------------------------------------------------
    # Essential Animation Methods - To be moved to animations.py later
    #-------------------------------------------------------------------------
    
    def power_on_animation(self):
        """Game Boy inspired power-on sequence."""
        # Placeholder - Will be moved to animations.py
        self.is_animating = True
        
        # Enable all buttons
        for button in self.buttons:
            button.config(state=tk.NORMAL)
        
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
    
    def animate_scanline(self):
        """Animate a CRT-style scanline effect."""
        # Only run animation in arcade mode when powered on
        if (not self.arcade_mode) or (not self.calculator.power_on and not self.is_animating):
            # Hide scanline and check again later at slower interval
            self.scan_line.place_forget()
            self.root.after(300, self.animate_scanline)
            return
                
        # Update scanline position at a slower pace
        screen_height = self.screen_frame.winfo_height()
        if screen_height > 10:  # Ensure screen has been rendered
            # Move scanline by 2px instead of 4px (slower movement)
            self.scan_line_pos = (self.scan_line_pos + 2) % screen_height
            self.scan_line.place(x=0, y=self.scan_line_pos, width=self.screen_frame.winfo_width())
        
        # Make the scanline more subtle and check less frequently
        self.scan_line.configure(height=2, bg=self.colors["accent1"])
        # Adjust transparency if your tkinter version supports it
        try:
            self.scan_line.configure(alpha=0.4)  # Make scanline semi-transparent
        except:
            pass
        
        # Continue animation at a slower refresh rate
        self.root.after(150, self.animate_scanline)  # 150ms instead of 50ms
        
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
        
    #-------------------------------------------------------------------------
    # Mode Toggle Methods
    #-------------------------------------------------------------------------
    
    def toggle_calculator_mode(self):
        """Toggle between arcade style and plain calculator."""
        # Toggle the mode
        self.arcade_mode = not self.arcade_mode
        
        # Update colors based on mode
        self.colors = ARCADE_COLORS if self.arcade_mode else BASIC_COLORS
        
        # Update button text
        if self.arcade_mode:
            self.mode_switch_btn.config(text="ARCADE MODE")
            self.enable_arcade_features()
        else:
            self.mode_switch_btn.config(text="BASIC MODE")
            self.disable_arcade_features()
            
        # Add transition animation
        self.mode_transition_animation()
    
    def enable_arcade_features(self):
        """Enable all arcade game features."""
        # Show face
        if hasattr(self, 'face'):
            self.face.face_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        # Show status bar elements - NEW ADDITION
        if hasattr(self, 'status_frame'):
            self.status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Enable animations
        self.is_animating = True
        
        # Restore game colors
        self.screen_frame.config(bg=self.colors["display_bg"])
        self.result_display.config(fg=self.colors["accent1"])
        self.title_label.config(text="CALC-BOY COLOR")
        
        # Re-enable scan line
        self.animate_scanline()

    def disable_arcade_features(self):
        """Disable arcade features for plain calculator mode."""
        # Hide face
        if hasattr(self, 'face'):
            self.face.face_frame.pack_forget()
        
        # Hide status bar elements - NEW ADDITION
        if hasattr(self, 'status_frame'):
            self.status_frame.pack_forget()
        
        # Disable animations
        self.is_animating = False
        
        # Simplify colors for basic mode
        self.screen_frame.config(bg="#111111")  # Dark but not pure black
        self.result_display.config(fg="#FFFFFF")  # White text
        self.title_label.config(text="BASIC CALC")
        
        # Hide scan line
        self.scan_line.place_forget()
    
    def mode_transition_animation(self):
        """Create a transition effect when switching modes."""
        # Store original display content
        original_result = self.result_display.cget("text")
        original_expr = self.expr_display.cget("text")
        
        # Flash the screen
        for i in range(3):
            self.screen_frame.config(bg="#FFFFFF")
            self.root.update()
            self.root.after(50)
            self.screen_frame.config(bg="#000000")
            self.root.update()
            self.root.after(50)
        
        # Display mode change message
        mode_text = "ARCADE MODE" if self.arcade_mode else "BASIC MODE"
        self.result_display.config(text=mode_text)
        self.expr_display.config(text="SWITCHING TO")
        
        # After delay, restore original content
        self.root.after(1000, lambda: (
            self.result_display.config(text=original_result),
            self.expr_display.config(text=original_expr)
        ))
        
    #-------------------------------------------------------------------------
    # Button Action Methods - Minimal implementations
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
        
        # React to power state change
        self.face.react_to_power_toggle(new_power_state)
        
        if new_power_state:
            self.power_on_animation()
        else:
            # Power off animation - placeholder
            self.flash_display()
            self.result_display.config(text="")
            self.expr_display.config(text="")
    
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
    
    def insert_function(self, func):
        """Insert a function into the expression and update display."""
        if not self.calculator.power_on:
            return
            
        # Update calculator state
        self.calculator.insert_function(func)
        
        # Update display
        self.expr_display.config(text=self.calculator.current_expression)
    
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
    
    def calculate(self):
        """Calculate the result of the expression."""
        if not self.calculator.power_on:
            return
            
        # Calculate expression - call the calculator logic's calculate method
        success, result, error = self.calculator.calculate()
        
        if success:
            # Increment calculation count and update score
            try:
                self.calc_count += 1
                if hasattr(self, 'score_label'):
                    self.score_label.config(text=f"CALCS: {self.calc_count}")
            except Exception as e:
                self.logger.error(f"Error updating calculation count: {e}")
            
            # Show result with animation
            self.flash_display()
            self.result_display.config(text=result)
            
            # Show face reaction
            self.face.react_to_calculation(result)
        else:
            # Show error
            self.flash_display()
            self.result_display.config(text="Error")
            self.expr_display.config(text=error)
            
            # Face reaction
            self.face.react_to_error(error)
    
    #-------------------------------------------------------------------------
    # Key Bindings
    #-------------------------------------------------------------------------
    
    def setup_key_bindings(self):
        """Set up keyboard shortcuts."""
        # Number keys
        for i in range(10):
            self.root.bind(str(i), lambda e, digit=i: self.handle_key_press(str(digit)))
        
        # Operation keys
        self.root.bind("+", lambda e: self.handle_key_press("+"))
        self.root.bind("-", lambda e: self.handle_key_press("-"))
        self.root.bind("*", lambda e: self.handle_key_press("×"))
        self.root.bind("/", lambda e: self.handle_key_press("÷"))
        self.root.bind("^", lambda e: self.handle_key_press("^"))
        self.root.bind("%", lambda e: self.handle_key_press("%"))
        self.root.bind(".", lambda e: self.handle_key_press("."))
        
        # Parentheses
        self.root.bind("(", lambda e: self.handle_key_press("("))
        self.root.bind(")", lambda e: self.handle_key_press(")"))
        
        # Control keys
        self.root.bind("<Return>", lambda e: self.calculate())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<Escape>", lambda e: self.all_clear())
        self.root.bind("<Delete>", lambda e: self.clear())
        
        # Function keys
        self.root.bind("<F1>", lambda e: self.toggle_power())
        self.root.bind("<F2>", lambda e: self.toggle_angle_mode("DEG"))
        self.root.bind("<F3>", lambda e: self.toggle_angle_mode("RAD"))
        self.root.bind("<F4>", lambda e: self.toggle_calculator_mode())
    
    def handle_key_press(self, key):
        """Handle keyboard input."""
        if not self.calculator.power_on:
            return
            
        # Update the calculator state for text input
        self.insert_text(key)