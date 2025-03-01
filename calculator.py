#!/usr/bin/env python3
"""
Game-Style Calculator - Core Calculator Logic
"""

import math
import logging

class Calculator:
    """
    Core calculator functionality handling mathematical operations.
    """
    
    def __init__(self):
        """Initialize calculator state and settings."""
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.info("Calculator logic initialized")
        
        # Calculator state
        self.current_expression = ""
        self.result = ""
        self.last_answer = "0"  # Store last calculated value
        self.memory_value = "0"  # M+ / M- memory functionality
        self.angle_mode = "DEG"  # DEG or RAD for trigonometric functions
        self.result_shown = False  # Flag if result is currently displayed
        self.power_on = False  # Power state
        
    def insert_text(self, text):
        """
        Add text to the current expression.
        
        Args:
            text (str): Text to be added to expression
            
        Returns:
            str: The updated expression
        """
        if not self.power_on:
            return self.current_expression
            
        if self.result_shown:
            if text in "0123456789.":
                self.current_expression = ""
            else:
                self.current_expression = self.result
            self.result_shown = False
        
        # Handle special constants
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
        
        Args:
            func (str): Function to be added (e.g., "sin(")
            
        Returns:
            str: The updated expression
        """
        if not self.power_on:
            return self.current_expression
            
        if self.result_shown:
            self.current_expression = ""
            self.result_shown = False
            
        self.current_expression += func
        return self.current_expression
        
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
        
        Returns:
            str: Updated expression after removing last character
        """
        if not self.power_on or self.result_shown:
            return self.current_expression
            
        if self.current_expression:
            # Check for functions to remove them completely
            functions = ["sin(", "cos(", "tan(", "sqrt(", "log("]
            for func in functions:
                if self.current_expression.endswith(func):
                    self.current_expression = self.current_expression[:-len(func)]
                    return self.current_expression
            
            # Regular backspace
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
    
    def memory_clear(self):
        """Clear the memory value."""
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
    
    def prepare_expression(self, expr):
        """
        Prepare the expression for evaluation by converting mathematical 
        notation to Python code.
        
        Args:
            expr (str): Raw mathematical expression
            
        Returns:
            str: Python-compatible expression ready for evaluation
        """
        # Replace mathematical symbols with Python operators
        expr = expr.replace("×", "*")
        expr = expr.replace("÷", "/")
        expr = expr.replace("^", "**")
        expr = expr.replace("π", "math.pi")
        expr = expr.replace("e", "math.e")
        
        # Handle percentage calculations
        expr = expr.replace("%", "/100")
        
        # Handle trigonometric functions based on angle mode
        if self.angle_mode == "DEG":
            expr = expr.replace("sin(", "math.sin(math.radians(")
            expr = expr.replace("cos(", "math.cos(math.radians(")
            expr = expr.replace("tan(", "math.tan(math.radians(")
            
            # Count special function occurrences to add closing parentheses later
            count_sin = expr.count("math.sin(math.radians(")
            count_cos = expr.count("math.cos(math.radians(")
            count_tan = expr.count("math.tan(math.radians(")
            expr = expr + ")" * (count_sin + count_cos + count_tan)
        else:
            expr = expr.replace("sin(", "math.sin(")
            expr = expr.replace("cos(", "math.cos(")
            expr = expr.replace("tan(", "math.tan(")
        
        # Handle other functions
        expr = expr.replace("sqrt(", "math.sqrt(")
        expr = expr.replace("log(", "math.log10(")
        
        return expr
    
    def calculate(self):
        """
        Evaluate the current expression and return the result.
        
        Returns:
            tuple: (success, result_string, error_message)
        """
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
            
            # Evaluate the expression
            self.logger.debug(f"Evaluating: {expr}")
            result = eval(expr)
            
            # Format the result
            if isinstance(result, int) or result == int(result):
                formatted_result = str(int(result))
            else:
                # Limit decimal places to avoid display overflow
                formatted_result = f"{result:.10g}"
            
            # Update calculator state
            self.result = formatted_result
            self.last_answer = formatted_result
            self.result_shown = True
            
            return True, formatted_result, ""
            
        except Exception as e:
            self.logger.error(f"Calculation error: {e}")
            return False, "Error", str(e)