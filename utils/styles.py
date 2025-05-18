"""
Game-Style Calculator - Styles and Theme
Centralized styling constants for the calculator application
"""

# Color schemes
ARCADE_COLORS = {
    "bg_dark": "#330000",        # Deeper, less intense red for background
    "bg_medium": "#660000",      # More subdued medium red
    "display_bg": "#000000",     # Keep black for display
    "accent1": "#FF3333",        # Slightly softer red accent
    "accent2": "#FF6666",        # Lighter accent with less intensity
    "accent3": "#990000",        # Richer dark red for buttons
    "accent4": "#222222",        # Same dark gray contrast
    "text_bright": "#FFFFFF",    # Keep white text
    "text_dim": "#CCCCCC",       # Lighter dim text for better readability
    "btn_shadow": "#220000"      # Same shadow color
}

BASIC_COLORS = {
    "bg_dark": "#222222",        # Dark gray background
    "bg_medium": "#333333",      # Medium gray
    "display_bg": "#111111",     # Nearly black display
    "accent1": "#FFFFFF",        # White primary accent
    "accent2": "#DDDDDD",        # Light gray secondary accent
    "accent3": "#999999",        # Medium gray accent
    "accent4": "#444444",        # Darker gray accent
    "text_bright": "#FFFFFF",    # White text
    "text_dim": "#BBBBBB",       # Dimmed text
    "btn_shadow": "#111111"      # Dark shadow
}

# Font definitions (to be used with tkinter.font.Font)
FONTS = {
    "display": {"family": "Press Start 2P", "size": 22, "weight": "bold"},
    "expression": {"family": "Press Start 2P", "size": 12},
    "button": {"family": "Press Start 2P", "size": 12},
    "small": {"family": "Press Start 2P", "size": 9},
    "title": {"family": "Press Start 2P", "size": 18},
    
    # Fallback fonts (used if pixel fonts aren't available)
    "fallback_display": {"family": "Courier", "size": 28, "weight": "bold"},
    "fallback_expression": {"family": "Courier", "size": 14},
    "fallback_button": {"family": "Courier", "size": 14, "weight": "bold"},
    "fallback_small": {"family": "Courier", "size": 10, "weight": "bold"},
    "fallback_title": {"family": "Courier", "size": 24, "weight": "bold"}
}

# Button configurations for the calculator
BUTTON_CONFIGS = [
    # Row 0
    [0, 0, "C", "clear", "accent1", "text_bright"],
    [0, 1, "AC", "all_clear", "accent1", "text_bright"],
    [0, 2, "(", "insert_text:(", "accent3", "text_bright"],
    [0, 3, ")", "insert_text:)", "accent3", "text_bright"],
    [0, 4, "←", "backspace", "accent4", "text_bright"],
    
    # Row 1
    [1, 0, "π", "insert_text:π", "accent3", "text_bright"],
    [1, 1, "sin", "insert_function:sin(", "accent3", "text_bright"],
    [1, 2, "cos", "insert_function:cos(", "accent3", "text_bright"],
    [1, 3, "tan", "insert_function:tan(", "accent3", "text_bright"],
    [1, 4, "^", "insert_text:^", "accent2", "display_bg"],
    
    # Row 2
    [2, 0, "7", "insert_text:7", "bg_medium", "text_bright"],
    [2, 1, "8", "insert_text:8", "bg_medium", "text_bright"],
    [2, 2, "9", "insert_text:9", "bg_medium", "text_bright"],
    [2, 3, "÷", "insert_text:÷", "accent2", "display_bg"],
    [2, 4, "√", "insert_function:sqrt(", "accent3", "text_bright"],
    
    # Row 3
    [3, 0, "4", "insert_text:4", "bg_medium", "text_bright"],
    [3, 1, "5", "insert_text:5", "bg_medium", "text_bright"],
    [3, 2, "6", "insert_text:6", "bg_medium", "text_bright"],
    [3, 3, "×", "insert_text:×", "accent2", "display_bg"],
    [3, 4, "%", "insert_text:%", "accent3", "text_bright"],
    
    # Row 4
    [4, 0, "1", "insert_text:1", "bg_medium", "text_bright"],
    [4, 1, "2", "insert_text:2", "bg_medium", "text_bright"],
    [4, 2, "3", "insert_text:3", "bg_medium", "text_bright"],
    [4, 3, "-", "insert_text:-", "accent2", "display_bg"],
    
    # Row 5
    [5, 0, "0", "insert_text:0", "bg_medium", "text_bright"],
    [5, 2, ".", "insert_text:.", "bg_medium", "text_bright"],
    [5, 3, "+", "insert_text:+", "accent2", "display_bg"],
]

# Animation configuration
ANIMATION = {
    "scan_line_speed": 50,       # Delay between scanline updates (ms)
    "scan_line_step": 4,         # Pixels per step for scanline
    "pulse_duration": 100,       # Duration of button pulse effect (ms)
    "pulse_interval": 2000,      # Time between automatic pulses (ms)
    "flash_duration": 50,        # Duration of display flash effect (ms)
    "boot_sequence_delay": 400,  # Delay between boot text frames (ms)
    "char_animation_delay": 50,  # Delay in character animation effects (ms)
    "wave_step_delay": 50,       # Delay between waves in button animations
}

# Easter egg configurations
EASTER_EGGS = {
    "konami_code": ["Up", "Up", "Down", "Down", "Left", "Right", "Left", "Right"],
    "secret_codes": {
        "123456": "matrix_mode",
        "31337": "hacker_mode",
        "80085": "silly_mode",
        "42": "answer_mode"
    }
}

# Face expressions for different moods
FACE_EXPRESSIONS = {
    "happy": "😊",
    "very_happy": "😄",
    "ecstatic": "🤩",
    "sad": "😔",
    "very_sad": "😢",
    "surprised": "😮",
    "shocked": "😱",
    "confused": "😕",
    "thinking": "🤔",
    "concentrating": "🧐",
    "excited": "🙌",
    "error": "😵",
    "cool": "😎",
    "super_cool": "🕶️",
    "wink": "😉",
    "smug": "😏",
    "evil_laugh": "😈",
    "meh": "😒",
    "tired": "😴",
    "nerd": "🤓",
    "default": "🙂"
}

# Emoji-enhanced operation reactions
OPERATION_REACTIONS = {
    "+": ("excited", "➕ Plus Ultra!"),
    "-": ("thinking", "➖ Calculating..."),
    "×": ("ecstatic", "✖️ Multiplying!"),
    "÷": ("concentrating", "➗ Dividing..."),
    "=": ("super_cool", "✨ Behold!"),
    "C": ("sad", "🧹 Swept away..."),
    "AC": ("shocked", "💥 All gone!"),
    "^": ("excited", "🚀 Powering up!"),
    "√": ("cool", "🔍 Finding roots!"),
    "%": ("thinking", "💯 Percenting!"),
    "sin": ("wink", "📐 Trigonometry!"),
    "cos": ("nerd", "📏 Cosine!"),
    "tan": ("cool", "📈 Tangent!"),
    "π": ("very_happy", "🥧 Pi time!")
    }