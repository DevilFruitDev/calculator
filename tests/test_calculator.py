"""
Unit tests for the Calculator class
Tests core calculation logic, operations, and error handling
"""

import unittest
import sys
import os
import math

# Add the parent directory to the path to import the calculator module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import Calculator


class TestCalculator(unittest.TestCase):
    """Test cases for the Calculator class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calc = Calculator()
        self.calc.power_on = True  # Ensure calculator is powered on for tests
    
    def tearDown(self):
        """Clean up after each test method."""
        self.calc = None
    
    # -------------------------------------------------------------------------
    # Basic Operations Tests
    # -------------------------------------------------------------------------
    
    def test_basic_addition(self):
        """Test basic addition operations."""
        self.calc.current_expression = "2+3"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, "5")
        
    def test_basic_subtraction(self):
        """Test basic subtraction operations."""
        self.calc.current_expression = "10-4"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, "6")
        
    def test_basic_multiplication(self):
        """Test basic multiplication operations."""
        self.calc.current_expression = "6×7"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, "42")
        
    def test_basic_division(self):
        """Test basic division operations."""
        self.calc.current_expression = "15÷3"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, "5")
    
    def test_decimal_operations(self):
        """Test operations with decimal numbers."""
        self.calc.current_expression = "2.5+1.5"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, "4")
        
    def test_negative_numbers(self):
        """Test operations with negative numbers."""
        self.calc.current_expression = "-5+3"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, "-2")
    
    # -------------------------------------------------------------------------
    # Complex Operations Tests
    # -------------------------------------------------------------------------
    
    def test_order_of_operations(self):
        """Test that order of operations is respected."""
        self.calc.current_expression = "2+3×4"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, "14")  # Should be 2+(3×4) = 14, not (2+3)×4 = 20
        
    def test_parentheses(self):
        """Test operations with parentheses."""
        self.calc.current_expression = "(2+3)×4"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, "20")
        
    def test_nested_parentheses(self):
        """Test nested parentheses."""
        self.calc.current_expression = "((2+1)×3)+4"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, "13")
    
    def test_power_operations(self):
        """Test power operations."""
        self.calc.current_expression = "2^3"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, "8")
        
    def test_square_root(self):
        """Test square root operations."""
        self.calc.current_expression = "sqrt(16)"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, "4")
        
    def test_percentage(self):
        """Test percentage operations."""
        self.calc.current_expression = "50%"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, "0.5")
    
    # -------------------------------------------------------------------------
    # Trigonometric Functions Tests
    # -------------------------------------------------------------------------
    
    def test_sin_degrees(self):
        """Test sine function in degrees mode."""
        self.calc.angle_mode = "DEG"
        self.calc.current_expression = "sin(30)"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        # sin(30°) = 0.5
        self.assertAlmostEqual(float(result), 0.5, places=5)
        
    def test_cos_degrees(self):
        """Test cosine function in degrees mode."""
        self.calc.angle_mode = "DEG"
        self.calc.current_expression = "cos(60)"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        # cos(60°) = 0.5
        self.assertAlmostEqual(float(result), 0.5, places=5)
        
    def test_tan_degrees(self):
        """Test tangent function in degrees mode."""
        self.calc.angle_mode = "DEG"
        self.calc.current_expression = "tan(45)"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        # tan(45°) = 1
        self.assertAlmostEqual(float(result), 1.0, places=5)
        
    def test_sin_radians(self):
        """Test sine function in radians mode."""
        self.calc.angle_mode = "RAD"
        self.calc.current_expression = f"sin({math.pi/2})"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        # sin(π/2) = 1
        self.assertAlmostEqual(float(result), 1.0, places=5)
    
    # -------------------------------------------------------------------------
    # Constants Tests
    # -------------------------------------------------------------------------
    
    def test_pi_constant(self):
        """Test pi constant."""
        self.calc.current_expression = "π"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertAlmostEqual(float(result), math.pi, places=5)
        
    def test_pi_in_calculation(self):
        """Test pi constant in calculations."""
        self.calc.current_expression = "2×π"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertAlmostEqual(float(result), 2 * math.pi, places=5)
    
    # -------------------------------------------------------------------------
    # Error Handling Tests
    # -------------------------------------------------------------------------
    
    def test_division_by_zero(self):
        """Test division by zero error handling."""
        self.calc.current_expression = "5÷0"
        success, result, error = self.calc.calculate()
        self.assertFalse(success)
        self.assertEqual(result, "Error")
        self.assertIn("division by zero", error.lower())
        
    def test_invalid_expression(self):
        """Test invalid expression error handling."""
        self.calc.current_expression = "2++"
        success, result, error = self.calc.calculate()
        self.assertFalse(success)
        self.assertEqual(result, "Error")
        
    def test_empty_expression(self):
        """Test empty expression handling."""
        self.calc.current_expression = ""
        success, result, error = self.calc.calculate()
        self.assertFalse(success)
        self.assertEqual(result, "")
        self.assertIn("No expression", error)
        
    def test_power_off_calculation(self):
        """Test calculation when calculator is powered off."""
        self.calc.power_on = False
        self.calc.current_expression = "2+2"
        success, result, error = self.calc.calculate()
        self.assertFalse(success)
    
    # -------------------------------------------------------------------------
    # State Management Tests
    # -------------------------------------------------------------------------
    
    def test_power_toggle(self):
        """Test power toggle functionality."""
        initial_state = self.calc.power_on
        new_state = self.calc.toggle_power()
        self.assertNotEqual(initial_state, new_state)
        self.assertEqual(self.calc.power_on, new_state)
        
    def test_angle_mode_setting(self):
        """Test angle mode setting."""
        self.calc.set_angle_mode("RAD")
        self.assertEqual(self.calc.angle_mode, "RAD")
        
        self.calc.set_angle_mode("DEG")
        self.assertEqual(self.calc.angle_mode, "DEG")
        
    def test_clear_functionality(self):
        """Test clear functionality."""
        self.calc.current_expression = "2+2"
        self.calc.clear()
        self.assertEqual(self.calc.current_expression, "")
        
    def test_all_clear_functionality(self):
        """Test all clear functionality."""
        self.calc.current_expression = "2+2"
        self.calc.result = "4"
        expr, result = self.calc.all_clear()
        self.assertEqual(expr, "")
        self.assertEqual(result, "0")
        
    def test_backspace_functionality(self):
        """Test backspace functionality."""
        self.calc.current_expression = "123"
        self.calc.backspace()
        self.assertEqual(self.calc.current_expression, "12")
        
    def test_insert_text(self):
        """Test text insertion."""
        self.calc.insert_text("2")
        self.calc.insert_text("+")
        self.calc.insert_text("3")
        self.assertEqual(self.calc.current_expression, "2+3")
        
    def test_insert_function(self):
        """Test function insertion."""
        self.calc.insert_function("sin(")
        self.assertEqual(self.calc.current_expression, "sin(")
    
    # -------------------------------------------------------------------------
    # Edge Cases Tests
    # -------------------------------------------------------------------------
    
    def test_very_large_numbers(self):
        """Test calculation with very large numbers."""
        self.calc.current_expression = "999999999×999999999"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertEqual(result, str(999999999 * 999999999))
        
    def test_very_small_numbers(self):
        """Test calculation with very small numbers."""
        self.calc.current_expression = "0.00001+0.00002"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        self.assertAlmostEqual(float(result), 0.00003, places=8)
        
    def test_auto_parentheses_closing(self):
        """Test automatic parentheses closing."""
        self.calc.current_expression = "((2+3)×4"
        success, result, error = self.calc.calculate()
        self.assertTrue(success)
        # Should auto-close the missing parenthesis
        self.assertEqual(result, "20")


if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    
    # Run the tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")