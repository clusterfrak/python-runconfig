"""
***************************************************************************
Unit Test:              Runconfig Globals Module Unit Tests
Authors/Maintainers:    Rich Nason (rnason@appcontainers.io)
Copyright:              Copyright 2016 Richard Nason
Description:            These Unit tests will tests the Globals Class to ensure proper code level functionality.
***************************************************************************
"""
# *******************************************************************
# Required Modules:
# *******************************************************************
import unittest
import os
from modules.globals import Globals


class GlobalTests(unittest.TestCase):
    """Tests for global.py"""

    def setUp(self):
        """Initialize the class, and instantiate a Globals instance"""
        # Instantiate the class
        self.global_variables = Globals()

    def test_is_rhel(self):
        """Check to see if this test is being ran on a rhel box"""
        print("Red Hat Based Distro: " + str(self.global_variables.is_rhel()))
        if os.path.isfile('/etc/redhat-release'):
            self.assertTrue(self.global_variables.is_rhel())
        else:
            self.assertFalse(self.global_variables.is_rhel())

if __name__ == '__main__':
    unittest.main()
