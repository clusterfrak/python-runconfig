"""
***************************************************************************
Unit Test:              Runconfig Mode Module Unit Tests
Authors/Maintainers:    Rich Nason (rnason@appcontainers.io)
Copyright:              Copyright 2016 Richard Nason
Description:            These Unit tests will tests the Mode Class to ensure proper code level functionality.
***************************************************************************
"""
# *******************************************************************
# Required Modules:
# *******************************************************************
import unittest
import os
from modules.mode import Mode


class ModeTests(unittest.TestCase):
    """Tests for mode.py"""

    def setUp(self):
        """Initialize the class, and instantiate a Mode instance"""
        self.testfile = "/tmp/testfile"

        # Create a test file
        open(self.testfile, 'w').close()

        # Instantiate the class
        self.mode = Mode()

    def test_config_verify(self):
        """Test the config verification, this checks for the existance of a file"""
        assert os.path.exists(self.testfile) == 1

        # Call the verification function passing it the test file, this should return true
        self.assertTrue(self.mode.config_verify(self.testfile))

        # Call the verification function passing it a bogus value, this should return false
        self.assertFalse(self.mode.config_verify("/etc/bogus.file"))

    def tearDown(self):
        """Cleanup test files that were created for the tests"""
        os.remove(self.testfile)

if __name__ == '__main__':
    unittest.main()
