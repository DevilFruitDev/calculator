#!/usr/bin/env python3
"""
Game-Style Calculator - Main Application Entry Point
"""

import tkinter as tk
import logging
from calculator import Calculator
from ui import CalculatorUI

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Create a logger for this module
    logger = logging.getLogger(__name__)
    logger.info("Application starting...")
    
    return logger

def main():
    """Main function to run the calculator application."""
    logger = setup_logging()
    
    # Create the main application window
    root = tk.Tk()
    root.title("Game-Style Calculator")
    
    # Create calculator logic instance
    calculator = Calculator()
    
    # Create UI with the calculator logic
    ui = CalculatorUI(root, calculator)
    
    # Start the application
    logger.info("Launching UI...")
    root.mainloop()
    
    logger.info("Application closed")

if __name__ == "__main__":
    main()