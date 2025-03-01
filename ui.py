#!/usr/bin/env python3
"""
Game-Style Calculator - User Interface
"""

import tkinter as tk
from tkinter import font
import logging
import time
import random

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
        
        # Color scheme
        self.colors = {
            "bg_dark": "#120458",        # Deep space blue
            "bg_medium": "#1B0E91",      # Medium blue
            "display_bg": "#000000",     # Black
            "accent1": "#FF2975",        # Neon pink
            "accent2": "#26CEFC",        # Cyan
            "accent3": "#9B5DE5",        # Purple
            "accent4": "#F15BB5",        # Pink
            "text_bright": "#FFFFFF",    # White
            "text_dim": "#AAAAAA",       # Light gray
            "btn_shadow": "#080230"      # Dark shadow
        }
        
        # Display animation variables
        self.anim_chars = "1234567890ABCDEF"
        self.is_animating = False
        self.scan_line_pos = 0
        
        self.root.configure(bg=self.colors["bg_dark"])
        
        # Create fonts
        self.create_fonts()
        
        # Create UI components
        self.create_ui()
        
        # Set up key bindings
        self.setup_key_bindings()
        
        # Start animations
        self.animate_scanline()
        
        # Start with powered off state
        self.root.after(500, self.power_on_animation)
    
    def create_fonts(self):
        """Create custom pixel-style fonts."""
        self.display_font = font.Font(family="Courier", size=28, weight="bold")
        self.expr_font = font.Font(family="Courier", size=14)
        self.button_font = font.Font(family="Courier", size=14, weight="bold")
        self.small_font = font.Font(family="Courier", size=10, weight="bold")
        self.title_font = font.Font(family="Courier", size=24, weight="bold")
    
    def create_ui(self):
        """Create all UI components."""
        self.create_arcade_cabinet()
        self.create_display()
        self.create_control_panel()
        self.create_buttons()
    
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
            text="CALC-ARCADE",
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
            bd=3,
            command=self.toggle_power
        )
        self.power_btn.pack(side=tk.RIGHT, padx=10)
    
    def create_buttons(self):
        """Create calculator buttons with video game styling."""
        # Main buttons panel designed like arcade controls
        self.buttons_panel = tk.Frame(
            self.cabinet_frame,
            bg=self.colors["bg_medium"],
            bd=10,
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
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create grid layout
        for i in range(5):
            self.buttons_frame.columnconfigure(i, weight=1)
        for i in range(5):
            self.buttons_frame.rowconfigure(i, weight=1)
            
        # Button definitions: [row, col, text, command, color, text_color]
        buttons = [
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
            
            # Row 5 (special case handling below)
            [5, 0, "0", lambda: self.insert_text("0"), self.colors["bg_medium"], self.colors["text_bright"]],
            [5, 2, ".", lambda: self.insert_text("."), self.colors["bg_medium"], self.colors["text_bright"]],
            [5, 3, "+", lambda: self.insert_text("+"), self.colors["accent2"], self.colors["display_bg"]],
        ]
        
        # Create and store button references for enabling/disabling
        self.buttons = []
        
        # Create each button with arcade style
        for btn in buttons:
            row, col, text, command, bg_color, fg_color = btn
            
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
                font=self.button_font,
                bg=bg_color,
                fg=fg_color,
                activebackground=fg_color,
                activeforeground=bg_color,
                relief=tk.RAISED,
                bd=4,
                command=command
            )
            button.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            self.buttons.append(button)
        
        # Special case for equals button
        equals_frame = tk.Frame(
            self.buttons_frame,
            bg=self.colors["btn_shadow"],
            bd=0,
            highlightthickness=0
        )
        equals_frame.grid(row=4, column=4, rowspan=2, padx=5, pady=5, sticky="nsew")
        
        equals_button = tk.Button(
            equals_frame,
            text="=",
            font=self.title_font,
            bg=self.colors["accent1"],
            fg=self.colors["text_bright"],
            activebackground=self.colors["text_bright"],
            activeforeground=self.colors["accent1"],
            relief=tk.RAISED,
            bd=4,
            command=self.calculate
        )
        equals_button.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.buttons.append(equals_button)
    
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
        
        if new_power_state:
            self.power_on_animation()
        else:
            self.power_off_animation()
    
    def power_on_animation(self):
        """Animated power-on sequence."""
        self.is_animating = True
        
        # Enable all buttons
        for button in self.buttons:
            button.config(state=tk.NORMAL)
        
        # Flash the title
        for _ in range(3):
            self.title_label.config(fg=self.colors["text_bright"])
            self.root.update()
            time.sleep(0.1)
            self.title_label.config(fg=self.colors["accent1"])
            self.root.update()
            time.sleep(0.1)
        
        # Boot sequence on the display
        boot_text = [
            "SYSTEM BOOT",
            "INITIALIZING...",
            "CALC OS v1.0",
            "READY."
        ]
        
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
    
    def handle_key(self, key):
        """Handle keyboard input."""
        if not self.calculator.power_on:
            return
            
        # Flash the corresponding button
        for i, button in enumerate(self.buttons):
            if button.cget("text") == key:
                self.pulse_button(i)
                break
        
        # Update the calculator state
        self.insert_text(key)
    
    def insert_text(self, text):
        """Insert text into the expression and update display."""
        if not self.calculator.power_on:
            return
            
        # Update calculator state
        self.calculator.insert_text(text)
        
        # Update display
        self.expr_display.config(text=self.calculator.current_expression)
        
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
        else:
            # Show error
            self.show_error_animation(error)
    
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
    
    def show_error_animation(self, error):
        """Show error with animation effects."""
        # Flash the display in error color
        self.screen_frame.config(bg=self.colors["accent1"])
        self.result_display.config(fg=self.colors["display_bg"])
        self.expr_display.config(fg=self.colors["display_bg"])
        
        # Show error message
        self.result_display.config(text="ERROR")
        self.expr_display.config(text=error[:20])  # Show first 20 chars of error
        
        # Blink effect
        for i in range(3):
            self.root.after(i*200, lambda: self.result_display.config(text=""))
            self.root.after(i*200+100, lambda: self.result_display.config(text="ERROR"))
        
        # Reset after delay
        self.root.after(600, lambda: (
            self.screen_frame.config(bg=self.colors["display_bg"]),
            self.result_display.config(fg=self.colors["accent1"]),
            self.expr_display.config(fg=self.colors["accent2"]),
            self.result_display.config(text="0")
        ))
    
    def play_click_sound(self):
        """Play a click sound effect (stub)."""
        # This is a stub for sound effects
        # In a real implementation, you might use pygame.mixer or another library
        pass
    
    # Additional features that could be implemented
    
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
        # This would add a calculation history panel
        # Implementation would include:
        # - A list or panel to show recent calculations
        # - Logic to store and recall calculation history
        # - Ability to click on a history item to recall it
        pass