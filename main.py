#!/usr/bin/env python3
"""
Game-Style Calculator - Main Application Entry Point
This file serves as the entry point for the arcade-style calculator application.
It initializes the necessary components and starts the UI.
"""

# Standard library imports a 
import tkinter as tk  # For building the GUI
import logging        # For application logging

# Local application imports
from calculator import Calculator  # Import the calculator logic module
from ui import CalculatorUI        # Import the user interface module

def setup_logging():
    """
    Configure logging for the application.
    
    This function sets up the logging configuration with timestamps, module names,
    and log levels to make debugging easier.
    
    Returns:
        logger: Configured logger instance for the main module
    """
    # Configure the basic logging parameters
    logging.basicConfig(
        level=logging.INFO,  # Set minimum log level to INFO (ignores DEBUG)
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format with timestamp, module, level and message
        datefmt="%Y-%m-%d %H:%M:%S"  # Date format for the timestamp
    )
    
    # Create a logger specific to this module
    logger = logging.getLogger(__name__)
    logger.info("Application starting...")  # Log application startup
    
    return logger

def main():
    """
    Main function to run the calculator application.
    
    This function serves as the application's entry point, setting up all
    required components and starting the main event loop.
    """
    # Set up logging first
    logger = setup_logging()
    
    # Create the main application window using tkinter
    root = tk.Tk()
    root.title("Game-Style Calculator")  # Set the window title
    
    # Create calculator logic instance
    # This handles all mathematical operations and calculator state
    calculator = Calculator()
    
    # Create UI with the calculator logic
    # This builds the arcade-style interface and connects it to the calculator logic
    ui = CalculatorUI(root, calculator)
    
    # Start the application by entering the tkinter event loop
    logger.info("Launching UI...")
    root.mainloop()  # This will block until the window is closed
    
    # This code will execute when the window is closed
    logger.info("Application closed")

# Standard Python idiom to only run the main function when executed as a script
# (not when imported as a module)
if __name__ == "__main__":
    main()
