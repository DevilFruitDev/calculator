# 🎮 Calc-Arcade: Game-Style Calculator

<div align="center">
  
![Calculator Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.6+-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

</div>

<p align="center">A retro arcade-inspired calculator with flashy animations and nostalgic design</p>

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Controls](#controls)
- [Functions](#functions)
- [Animation Effects](#animation-effects)
- [Technical Details](#technical-details)
- [Dependencies](#dependencies)
- [Future Updates](#future-updates)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Calc-Arcade combines mathematical functionality with retro gaming aesthetics. This application reimagines the everyday calculator as an 80s/90s arcade cabinet, complete with neon colors, pixel-style fonts, and nostalgic animations.

<div align="center">
  <i>Screenshot coming soon</i>
</div>

---

## ✨ Features

- **Arcade Cabinet Design**: Styled to look like a vintage arcade machine
- **CRT Display Effects**: Including animated scanlines and screen glow
- **Boot Sequence**: Power on/off animations with startup messages
- **Math Operations**: Complete set of basic and scientific functions
- **Animated Feedback**: Visual reactions to calculations and errors
- **Memory Functions**: Store and recall values for complex calculations
- **Angle Modes**: Switch between degrees and radians for trigonometry

---

## 📥 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/calc-arcade.git

# Navigate to the project directory
cd calc-arcade

# Run the application
python main.py
```

### Requirements
- Python 3.6 or higher
- Tkinter (included in standard Python distribution)

---

## 🎮 Usage

1. Launch the application using `python main.py`
2. The calculator will start in powered-off state
3. Click the **POWER** button or press **F1** to boot up
4. Use mouse clicks or keyboard input to perform calculations
5. Toggle between DEG/RAD mode for trigonometric functions

---

## 🕹️ Controls

| Action | Mouse | Keyboard |
|--------|-------|----------|
| Numbers | Click buttons | Number keys (0-9) |
| Operations | Click +, -, ×, ÷ | +, -, *, / |
| Calculate | Click = | Enter |
| Clear | Click C | Delete |
| All Clear | Click AC | Escape |
| Backspace | Click ← | Backspace |
| Power | Click POWER | F1 |
| Mode | Click DEG/RAD | F2/F3 |

---

## 🧮 Functions

- **Basic Operations**: Addition, subtraction, multiplication, division
- **Scientific Functions**: 
  - Trigonometric: `sin`, `cos`, `tan`
  - Other: Square root (`√`), Power (`^`), Percentage (`%`)
- **Constants**: π (pi)
- **Memory Operations**: Memory Clear (MC), Memory Recall (MR), Memory Add (M+), Memory Subtract (M-)
- **Mode Switching**: Degrees/Radians toggle for angle calculations

---

## ✨ Animation Effects

- **Power Sequences**: Startup and shutdown animations
- **CRT Effects**: Moving scanline and screen flicker
- **Feedback Animations**: 
  - Flash effects when performing calculations
  - Shake effect for errors
  - Special animations for interesting results
- **Button Interactions**: Visual feedback when pressing buttons
- **Idle Animations**: Periodic effects when calculator is inactive

---

## 🔧 Technical Details

The application follows a modular structure:

- **calculator.py**: Core calculation logic
- **ui.py**: Visual interface components and animations
- **main.py**: Application entry point and configuration

The UI is built with Tkinter using custom styling to achieve the retro arcade aesthetic.

---

## 📚 Dependencies

- Python 3.6+
- Tkinter (included in standard Python distribution)
- Math library (standard)

---

## 🚀 Future Updates

- Custom themes and color schemes
- Sound effects and audio feedback
- Persistent calculation history
- Additional mathematical functions
- Graphing capabilities
- Matrix operations
- Easter egg animations and secrets
- Performance optimizations
- Expanded keyboard shortcuts
- User preferences saving

*Last updated: March 2025*

---

## 👥 Contributing

Currently in development. Contributions, suggestions, and feedback are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  <p>Created with ❤️ by YourName</p>
  <p>© 2025 - All Rights Reserved</p>
</div>
