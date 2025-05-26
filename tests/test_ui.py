"""
Unit tests for UI components
Tests UI logic, face expressions, and component interactions
"""

import unittest
import sys
import os
import tkinter as tk
from unittest.mock import Mock, MagicMock, patch

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.components.calculator_face import CalculatorFace
from utils.styles import FACE_EXPRESSIONS, OPERATION_REACTIONS, ARCADE_COLORS
from calculator import Calculator


class TestCalculatorFace(unittest.TestCase):
    """Test cases for the CalculatorFace component."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a mock parent frame to avoid actual GUI creation
        self.mock_parent = Mock()
        self.mock_parent.after = Mock()
        
        # Mock colors
        self.colors = ARCADE_COLORS
        
        # Create face instance with mocked components
        with patch('tkinter.Frame'), patch('tkinter.Label'), patch('tkinter.Canvas'):
            self.face = CalculatorFace(self.mock_parent, self.colors)
            
            # Mock the UI components
            self.face.face_display = Mock()
            self.face.bubble_text = Mock()
            self.face.bubble_frame = Mock()
    
    def tearDown(self):
        """Clean up after each test method."""
        self.face = None
    
    # -------------------------------------------------------------------------
    # Expression Display Tests
    # -------------------------------------------------------------------------
    
    def test_show_expression_happy(self):
        """Test showing happy expression."""
        self.face.show_expression("happy", "Test message")
        
        # Verify face display was updated with correct expression
        expected_face = FACE_EXPRESSIONS["happy"]
        self.face.face_display.config.assert_called_with(text=expected_face)
        
        # Verify bubble text was updated
        self.face.bubble_text.config.assert_called_with(text="Test message")
    
    def test_show_expression_without_message(self):
        """Test showing expression without message."""
        self.face.show_expression("sad")
        
        # Verify face display was updated
        expected_face = FACE_EXPRESSIONS["sad"]
        self.face.face_display.config.assert_called_with(text=expected_face)
    
    def test_show_expression_unknown_mood(self):
        """Test showing expression with unknown mood falls back to default."""
        self.face.show_expression("unknown_mood")
        
        # Should use default expression
        expected_face = FACE_EXPRESSIONS["default"]
        self.face.face_display.config.assert_called_with(text=expected_face)
    
    # -------------------------------------------------------------------------
    # Calculation Reaction Tests  
    # -------------------------------------------------------------------------
    
    def test_react_to_calculation_answer_42(self):
        """Test reaction to the answer 42."""
        self.face.react_to_calculation("42")
        
        # Should show cool expression with special message
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["cool"])
    
    def test_react_to_calculation_zero(self):
        """Test reaction to zero result."""
        self.face.react_to_calculation("0")
        
        # Should show thinking expression
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["thinking"])
    
    def test_react_to_calculation_pi(self):
        """Test reaction to pi approximation."""
        self.face.react_to_calculation("3.14159")
        
        # Should show happy expression for pi
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["happy"])
    
    def test_react_to_calculation_negative(self):
        """Test reaction to negative numbers."""
        self.face.react_to_calculation("-5")
        
        # Should show sad expression
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["sad"])
    
    def test_react_to_calculation_large_number(self):
        """Test reaction to very large numbers."""
        self.face.react_to_calculation("9001")
        
        # Should show surprised expression for >9000
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["surprised"])
    
    def test_react_to_calculation_easter_eggs(self):
        """Test reactions to easter egg numbers."""
        # Test 69
        self.face.react_to_calculation("69")
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["wink"])
        
        # Test 420
        self.face.react_to_calculation("420")
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["wink"])
    
    def test_react_to_calculation_huge_number(self):
        """Test reaction to million+ numbers."""
        self.face.react_to_calculation("1000001")
        
        # Should show excited expression
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["excited"])
    
    def test_react_to_calculation_error_result(self):
        """Test reaction to error results."""
        self.face.react_to_calculation("ERROR")
        
        # Should show error expression
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["error"])
    
    def test_react_to_calculation_non_numeric(self):
        """Test reaction to non-numeric results."""
        self.face.react_to_calculation("invalid")
        
        # Should show confused expression
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["confused"])
    
    # -------------------------------------------------------------------------
    # Operation Reaction Tests
    # -------------------------------------------------------------------------
    
    def test_react_to_operation_addition(self):
        """Test reaction to addition operation."""
        self.face.react_to_operation("+")
        
        # Should show happy expression with adding message
        expected_mood, expected_message = OPERATION_REACTIONS["+"]
        expected_face = FACE_EXPRESSIONS[expected_mood]
        self.face.face_display.config.assert_called_with(text=expected_face)
    
    def test_react_to_operation_multiplication(self):
        """Test reaction to multiplication operation."""
        self.face.react_to_operation("×")
        
        # Should show excited expression
        expected_mood, expected_message = OPERATION_REACTIONS["×"]
        expected_face = FACE_EXPRESSIONS[expected_mood]
        self.face.face_display.config.assert_called_with(text=expected_face)
    
    def test_react_to_operation_equals(self):
        """Test reaction to equals operation."""
        self.face.react_to_operation("=")
        
        # Should show very happy expression
        expected_mood, expected_message = OPERATION_REACTIONS["="]
        expected_face = FACE_EXPRESSIONS[expected_mood]
        self.face.face_display.config.assert_called_with(text=expected_face)
    
    def test_react_to_operation_clear(self):
        """Test reaction to clear operation."""
        self.face.react_to_operation("C")
        
        # Should show sad expression
        expected_mood, expected_message = OPERATION_REACTIONS["C"]
        expected_face = FACE_EXPRESSIONS[expected_mood]
        self.face.face_display.config.assert_called_with(text=expected_face)
    
    def test_react_to_operation_pi(self):
        """Test reaction to pi operation."""
        self.face.react_to_operation("π")
        
        # Should show happy expression
        expected_mood, expected_message = OPERATION_REACTIONS["π"]
        expected_face = FACE_EXPRESSIONS[expected_mood]
        self.face.face_display.config.assert_called_with(text=expected_face)
    
    def test_react_to_operation_unknown(self):
        """Test reaction to unknown operation."""
        # This should not cause any error, just not react
        try:
            self.face.react_to_operation("unknown")
        except KeyError:
            self.fail("react_to_operation should handle unknown operations gracefully")
    
    # -------------------------------------------------------------------------
    # Error Reaction Tests
    # -------------------------------------------------------------------------
    
    def test_react_to_error_division_by_zero(self):
        """Test reaction to division by zero error."""
        self.face.react_to_error("division by zero")
        
        # Should show error expression with specific message
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["error"])
    
    def test_react_to_error_syntax(self):
        """Test reaction to syntax error."""
        self.face.react_to_error("syntax error")
        
        # Should show confused expression
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["confused"])
    
    def test_react_to_error_generic(self):
        """Test reaction to generic error."""
        self.face.react_to_error("generic error")
        
        # Should show error expression
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["error"])
    
    # -------------------------------------------------------------------------
    # Power Toggle Tests
    # -------------------------------------------------------------------------
    
    def test_react_to_power_on(self):
        """Test reaction to power being turned on."""
        self.face.react_to_power_toggle(True)
        
        # Should show excited expression
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["excited"])
    
    def test_react_to_power_off(self):
        """Test reaction to power being turned off."""
        self.face.react_to_power_toggle(False)
        
        # Should show sad expression
        self.face.face_display.config.assert_called_with(text=FACE_EXPRESSIONS["sad"])


class TestStylesConfiguration(unittest.TestCase):
    """Test cases for styles configuration."""
    
    def test_face_expressions_completeness(self):
        """Test that all required face expressions are defined."""
        required_expressions = [
            "happy", "very_happy", "sad", "surprised", "confused", 
            "thinking", "excited", "error", "cool", "wink", "default"
        ]
        
        for expression in required_expressions:
            self.assertIn(expression, FACE_EXPRESSIONS, 
                         f"Missing face expression: {expression}")
    
    def test_operation_reactions_completeness(self):
        """Test that all basic operations have reactions defined."""
        required_operations = ["+", "-", "×", "÷", "=", "C", "AC", "^", "√", "%", "π"]
        
        for operation in required_operations:
            self.assertIn(operation, OPERATION_REACTIONS,
                         f"Missing operation reaction: {operation}")
    
    def test_operation_reactions_format(self):
        """Test that operation reactions have correct format."""
        for operation, reaction in OPERATION_REACTIONS.items():
            self.assertIsInstance(reaction, tuple, 
                                f"Reaction for {operation} should be a tuple")
            self.assertEqual(len(reaction), 2,
                           f"Reaction for {operation} should have mood and message")
            
            mood, message = reaction
            self.assertIn(mood, FACE_EXPRESSIONS,
                         f"Mood '{mood}' for operation '{operation}' not in FACE_EXPRESSIONS")
            self.assertIsInstance(message, str,
                                f"Message for operation '{operation}' should be a string")
    
    def test_arcade_colors_completeness(self):
        """Test that all required color keys are present."""
        required_colors = [
            "bg_dark", "bg_medium", "display_bg", "accent1", "accent2", 
            "accent3", "accent4", "text_bright", "text_dim", "btn_shadow"
        ]
        
        for color_key in required_colors:
            self.assertIn(color_key, ARCADE_COLORS,
                         f"Missing color key: {color_key}")
    
    def test_color_format(self):
        """Test that color values are in correct format."""
        for color_key, color_value in ARCADE_COLORS.items():
            self.assertIsInstance(color_value, str,
                                f"Color {color_key} should be a string")
            self.assertTrue(color_value.startswith("#"),
                          f"Color {color_key} should start with #")
            self.assertEqual(len(color_value), 7,
                           f"Color {color_key} should be 7 characters long")


class TestUIIntegration(unittest.TestCase):
    """Integration tests for UI components."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calculator = Calculator()
        self.calculator.power_on = True
    
    def test_calculator_face_integration(self):
        """Test integration between calculator and face components."""
        # Mock UI components
        mock_parent = Mock()
        mock_parent.after = Mock()
        
        with patch('tkinter.Frame'), patch('tkinter.Label'), patch('tkinter.Canvas'):
            face = CalculatorFace(mock_parent, ARCADE_COLORS)
            face.face_display = Mock()
            face.bubble_text = Mock()
            face.bubble_frame = Mock()
            
            # Test calculation workflow
            self.calculator.current_expression = "2+2"
            success, result, error = self.calculator.calculate()
            
            if success:
                face.react_to_calculation(result)
                # Should have called face_display.config
                face.face_display.config.assert_called()
    
    def test_error_handling_integration(self):
        """Test error handling integration between calculator and UI."""
        mock_parent = Mock()
        mock_parent.after = Mock()
        
        with patch('tkinter.Frame'), patch('tkinter.Label'), patch('tkinter.Canvas'):
            face = CalculatorFace(mock_parent, ARCADE_COLORS)
            face.face_display = Mock()
            face.bubble_text = Mock()
            face.bubble_frame = Mock()
            
            # Test error workflow
            self.calculator.current_expression = "1÷0"
            success, result, error = self.calculator.calculate()
            
            if not success:
                face.react_to_error(error)
                # Should have called face_display.config with error expression
                face.face_display.config.assert_called()


if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestCalculatorFace))
    suite.addTests(loader.loadTestsFromTestCase(TestStylesConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestUIIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"UI Tests Summary")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"\nSuccess rate: {success_rate:.1f}%")
    print(f"{'='*50}")