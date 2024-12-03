import unittest
from tests.test_auth import TestAuthentication
from tests.test_pi import TestPiCalculation
from tests.test_legacy import TestLegacyService
from tests.test_statistics import TestStatistics
from tests.test_tasks import TestTaskManagement

def run_tests():
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAuthentication))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPiCalculation))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLegacyService))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStatistics))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTaskManagement))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)

if __name__ == '__main__':
    run_tests()