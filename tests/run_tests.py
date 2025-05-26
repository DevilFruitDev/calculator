#!/usr/bin/env python3
"""
Test runner for the Calc-Arcade calculator application.
Runs all unit tests and provides a comprehensive summary.
"""

import unittest
import sys
import os
import time
from io import StringIO

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test modules
from tests.test_calculator import TestCalculator
from tests.test_ui import TestCalculatorFace, TestStylesConfiguration, TestUIIntegration


class ColoredTextTestResult(unittest.TextTestResult):
    """Custom test result class with colored output."""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.success_count = 0
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.success_count += 1
        if self.verbosity > 1:
            self.stream.write("✅ ")
            self.stream.writeln(f"{test._testMethodName}")
    
    def addError(self, test, err):
        super().addError(test, err)
        if self.verbosity > 1:
            self.stream.write("❌ ")
            self.stream.writeln(f"{test._testMethodName} - ERROR")
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        if self.verbosity > 1:
            self.stream.write("❌ ")
            self.stream.writeln(f"{test._testMethodName} - FAILED")


class ColoredTextTestRunner(unittest.TextTestRunner):
    """Custom test runner with colored output."""
    
    resultclass = ColoredTextTestResult


def run_test_suite(test_class, suite_name):
    """Run a specific test suite and return results."""
    print(f"\n🧪 Running {suite_name} Tests...")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(test_class)
    
    # Run tests
    stream = StringIO()
    runner = ColoredTextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    # Print results
    output = stream.getvalue()
    print(output)
    
    return result


def main():
    """Main test runner function."""
    print("🎮 CALC-ARCADE TEST SUITE")
    print("=" * 60)
    print("Running comprehensive tests for the calculator application...")
    
    start_time = time.time()
    all_results = []
    
    # Test suites to run
    test_suites = [
        (TestCalculator, "Calculator Logic"),
        (TestCalculatorFace, "Calculator Face UI"),
        (TestStylesConfiguration, "Styles Configuration"),
        (TestUIIntegration, "UI Integration")
    ]
    
    # Run each test suite
    for test_class, suite_name in test_suites:
        try:
            result = run_test_suite(test_class, suite_name)
            all_results.append((suite_name, result))
        except Exception as e:
            print(f"❌ Error running {suite_name} tests: {e}")
            continue
    
    # Calculate overall statistics
    total_tests = sum(result.testsRun for _, result in all_results)
    total_failures = sum(len(result.failures) for _, result in all_results)
    total_errors = sum(len(result.errors) for _, result in all_results)
    total_success = total_tests - total_failures - total_errors
    
    # Print comprehensive summary
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n🏁 COMPREHENSIVE TEST SUMMARY")
    print("=" * 60)
    
    # Per-suite breakdown
    for suite_name, result in all_results:
        success_count = result.testsRun - len(result.failures) - len(result.errors)
        success_rate = (success_count / result.testsRun * 100) if result.testsRun > 0 else 0
        
        status = "✅ PASSED" if len(result.failures) == 0 and len(result.errors) == 0 else "❌ FAILED"
        print(f"{suite_name:25} | {success_count:2}/{result.testsRun:2} | {success_rate:5.1f}% | {status}")
    
    print("-" * 60)
    
    # Overall statistics
    overall_success_rate = (total_success / total_tests * 100) if total_tests > 0 else 0
    
    print(f"📊 OVERALL STATISTICS:")
    print(f"   Total Tests:     {total_tests}")
    print(f"   ✅ Passed:       {total_success}")
    print(f"   ❌ Failed:       {total_failures}")
    print(f"   🚫 Errors:       {total_errors}")
    print(f"   ⏱️  Duration:     {duration:.2f} seconds")
    print(f"   📈 Success Rate: {overall_success_rate:.1f}%")
    
    # Final status
    if total_failures == 0 and total_errors == 0:
        print(f"\n🎉 ALL TESTS PASSED! Your calculator is ready for deployment! 🚀")
        return_code = 0
    else:
        print(f"\n⚠️  SOME TESTS FAILED. Please review the failures above.")
        return_code = 1
    
    print("\n" + "=" * 60)
    return return_code


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)