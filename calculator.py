#!/usr/bin/env python3
"""
Game-Style Calculator - Core Calculator Logic
This module contains the core mathematical functionality and state management
for the calculator application.
"""

# Standard library imports
import math       # For mathematical functions
import logging    # For application logging

class Calculator:
    """
    Core calculator functionality handling mathematical operations.
    
    This class manages the calculator's state and handles all mathematical
    operations, expression parsing, and result formatting.
    """
    
    def __init__(self):
        """
        Initialize calculator state and settings.
        
        Sets up initial values for all calculator properties and configures logging.
        """
        # Set up logging for this class
        self.logger = logging.getLogger(__name__)
        self.logger.info("Calculator logic initialized")
        
        # Calculator state variables
        self.current_expression = ""     # The expression being built
        self.result = ""                 # The last calculated result
        self.last_answer = "0"           # Store last calculated value for ANS functionality
        self.memory_value = "0"          # Memory storage for M+/M- functionality
        self.angle_mode = "DEG"          # Angle mode: DEG (degrees) or RAD (radians)
        self.result_shown = False        # Flag indicating if result is currently displayed
        self.power_on = False            # Power state of the calculator
        
    #-------------------------------------------------------------------------
    # Input Handling Methods
    #-------------------------------------------------------------------------
    
    def insert_text(self, text):
        """
        Add text to the current expression.
        
        Handles special cases like starting a new calculation after showing a result,
        and properly formatting special constants like π and e.
        
        Args:
            text (str): Text to be added to expression
            
        Returns:
            str: The updated expression
        """
        # Do nothing if calculator is powered off
        if not self.power_on:
            return self.current_expression
        
        # Handle special case: when result is shown and user inputs something new
        if self.result_shown:
            # For digits and decimal point, start a new expression
            if text in "0123456789.":
                self.current_expression = ""
            # For operators, use the previous result as the first operand
            else:
                self.current_expression = self.result
            self.result_shown = False
        
        # Handle special mathematical constants
        if text == "π":
            self.current_expression += "π"
        elif text == "e":
            self.current_expression += "e"
        else:
            self.current_expression += text
            
        return self.current_expression
    
    def insert_function(self, func):
        """
        Add a function to the current expression.
        
        Handles functions like sin, cos, tan, etc.
        
        Args:
            func (str): Function to be added (e.g., "sin(")
            
        Returns:
            str: The updated expression
        """
        # Do nothing if calculator is powered off
        if not self.power_on:
            return self.current_expression
        
        # Handle special case: when result is shown and user inputs a function
        if self.result_shown:
            self.current_expression = ""
            self.result_shown = False
            
        self.current_expression += func
        return self.current_expression
    
    #-------------------------------------------------------------------------
    # Editing and State Management Methods
    #-------------------------------------------------------------------------
    
    def clear(self):
        """
        Clear the current expression.
        
        Returns:
            str: Empty string
        """
        self.current_expression = ""
        return self.current_expression
        
    def all_clear(self):
        """
        Clear everything (expression, result, last answer).
        
        Returns:
            tuple: (empty expression, "0" result)
        """
        self.current_expression = ""
        self.result = ""
        self.last_answer = "0"
        self.result_shown = False
        return self.current_expression, "0"
        
    def backspace(self):
        """
        Remove the last character from the expression.
        
        Intelligently handles functions - removes the entire function name
        rather than just one character.
        
        Returns:
            str: Updated expression after removing last character
        """
        # Do nothing if calculator is powered off or showing result
        if not self.power_on or self.result_shown:
            return self.current_expression
            
        if self.current_expression:
            # Check for functions to remove them completely
            functions = ["sin(", "cos(", "tan(", "sqrt(", "log("]
            for func in functions:
                if self.current_expression.endswith(func):
                    self.current_expression = self.current_expression[:-len(func)]
                    return self.current_expression
            
            # Regular backspace - remove last character
            self.current_expression = self.current_expression[:-1]
            
        return self.current_expression
    
    def set_angle_mode(self, mode):
        """
        Set the angle mode for trigonometric calculations.
        
        Args:
            mode (str): "DEG" or "RAD"
            
        Returns:
            str: The current mode
        """
        if mode in ["DEG", "RAD"]:
            self.angle_mode = mode
            self.logger.info(f"Angle mode set to {mode}")
        return self.angle_mode
    
    def toggle_power(self):
        """
        Toggle the calculator's power state.
        
        Clears state when powering off.
        
        Returns:
            bool: The new power state
        """
        self.power_on = not self.power_on
        self.logger.info(f"Power toggled: {self.power_on}")
        
        # Clear state when powering off
        if not self.power_on:
            self.current_expression = ""
            self.result = ""
            
        return self.power_on
    
    #-------------------------------------------------------------------------
    # Memory Operations
    #-------------------------------------------------------------------------
    
    def memory_clear(self):
        """
        Clear the memory value.
        
        Sets memory to "0".
        """
        self.memory_value = "0"
        self.logger.info("Memory cleared")
        
    def memory_recall(self):
        """
        Recall the memory value and add it to the expression.
        
        Returns:
            str: The updated expression
        """
        if self.result_shown:
            self.current_expression = ""
            self.result_shown = False
            
        self.current_expression += self.memory_value
        return self.current_expression
        
    def memory_add(self):
        """
        Add the current result to memory.
        
        Returns:
            str: The new memory value
        """
        if self.result:
            try:
                memory = float(self.memory_value)
                current = float(self.result)
                self.memory_value = str(memory + current)
                self.logger.info(f"Added to memory: {self.memory_value}")
            except ValueError:
                self.logger.error("Memory add failed: invalid values")
        return self.memory_value
                
    def memory_subtract(self):
        """
        Subtract the current result from memory.
        
        Returns:
            str: The new memory value
        """
        if self.result:
            try:
                memory = float(self.memory_value)
                current = float(self.result)
                self.memory_value = str(memory - current)
                self.logger.info(f"Subtracted from memory: {self.memory_value}")
            except ValueError:
                self.logger.error("Memory subtract failed: invalid values")
        return self.memory_value
    
    #-------------------------------------------------------------------------
    # Expression Evaluation Methods
    #-------------------------------------------------------------------------
    
    def prepare_expression(self, expr):
        """
        Prepare the expression for evaluation by converting mathematical 
        notation to Python code.
        
        Handles conversions like × to *, π to math.pi, etc., and properly
        formats trigonometric functions based on the current angle mode.
        
        Args:
            expr (str): Raw mathematical expression
            
        Returns:
            str: Python-compatible expression ready for evaluation
        """
        # Replace mathematical symbols with Python operators
        expr = expr.replace("×", "*")        # Multiplication symbol
        expr = expr.replace("÷", "/")        # Division symbol
        expr = expr.replace("^", "**")       # Exponentiation
        expr = expr.replace("π", "math.pi")  # Pi constant
        expr = expr.replace("e", "math.e")   # Euler's number
        
        # Handle percentage calculations
        expr = expr.replace("%", "/100")
        
        # Handle trigonometric functions based on angle mode
        if self.angle_mode == "DEG":
            # In degrees mode, convert degrees to radians before applying trig functions
            expr = expr.replace("sin(", "math.sin(math.radians(")
            expr = expr.replace("cos(", "math.cos(math.radians(")
            expr = expr.replace("tan(", "math.tan(math.radians(")
            
            # Count special function occurrences to add closing parentheses later
            count_sin = expr.count("math.sin(math.radians(")
            count_cos = expr.count("math.cos(math.radians(")
            count_tan = expr.count("math.tan(math.radians(")
            expr = expr + ")" * (count_sin + count_cos + count_tan)
        else:
            # In radians mode, use trig functions directly
            expr = expr.replace("sin(", "math.sin(")
            expr = expr.replace("cos(", "math.cos(")
            expr = expr.replace("tan(", "math.tan(")
        
        # Handle other mathematical functions
        expr = expr.replace("sqrt(", "math.sqrt(")
        expr = expr.replace("log(", "math.log10(")
        
        return expr
    
    def calculate(self):
        """
        Evaluate the current expression and return the result.
        
        Handles expression preparation, evaluation, error handling,
        and result formatting.
        
        Returns:
            tuple: (success, result_string, error_message)
        """
        # Check if calculator is on and has an expression to evaluate
        if not self.power_on or not self.current_expression:
            return False, "", "No expression to calculate"
        
        try:
            # Prepare the expression for evaluation
            expr = self.prepare_expression(self.current_expression)
            
            # Add proper closing parentheses if needed
            open_parens = expr.count("(")
            close_parens = expr.count(")")
            if open_parens > close_parens:
                expr += ")" * (open_parens - close_parens)
            
            # Evaluate the expression using Python's eval function
            self.logger.debug(f"Evaluating: {expr}")
            result = eval(expr)
            
            # Format the result
            if isinstance(result, int) or result == int(result):
                # For integers or values that are effectively integers
                formatted_result = str(int(result))
            else:
                # For floating point values, limit decimal places
                formatted_result = f"{result:.10g}"
            
            # Update calculator state
            self.result = formatted_result
            self.last_answer = formatted_result
            self.result_shown = True
            
            return True, formatted_result, ""
            
        except Exception as e:
            # Handle any errors during evaluation
            self.logger.error(f"Calculation error: {e}")
            return False, "Error", str(e)