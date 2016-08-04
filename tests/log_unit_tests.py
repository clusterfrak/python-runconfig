"""
***************************************************************************
Unit Test:              Runconfig Log Module Unit Tests
Authors/Maintainers:    Rich Nason (rnason@appcontainers.io)
Copyright:              Copyright 2016 Richard Nason
Description:            These Unit tests will tests the Log Class to ensure proper code level functionality.
***************************************************************************
"""
# *******************************************************************
# Required Modules:
# *******************************************************************
import unittest
import os
from modules.log import Log


class LogTests(unittest.TestCase):
    """Tests for log.py"""

    def setUp(self):
        """Initialize the class, and instantiate a Log instance"""
        self.logfile = "/var/log/docker/install.log"
        self.install_log = Log()

    def test_logfile(self):
        """Test the logfile file path and ensure that the file exists"""
        assert os.path.exists(self.logfile) == 1

    def test_write_log(self):
        """Test the log writing method to ensure that it writes to the log file properly"""
        # Clear the file in the event that any data is already in it
        open(self.logfile, 'w').close()

        # Call the method to write something to the file
        self.install_log.write_log("Test1")

        with open(self.logfile, "r") as logfile:
            logs = logfile.readlines()
            logfile.close()

        for line in logs:
            self.assertIn('Test1', line, msg="Log message was not properly written to the logfile.")

    def test_write_log_console(self):
        """Test the log writing method to ensure that it writes to the log file properly"""
        # Clear the file in the event that any data is already in it
        open(self.logfile, 'w').close()

        # Call the method to write something to the file
        self.install_log.write_log_console("Test2", "Test3")

        with open(self.logfile, "r") as logfile:
            logs = logfile.readlines()
            logfile.close()

        self.assertIn('Test2', logs[2], msg="Log message was not properly written to the logfile.")
        self.assertIn('Test3', logs[3], msg="Log message was not properly written to the logfile.")

    def test_step_complete(self):
        """Test the log writing method to ensure that it writes to the log file properly"""
        # Clear the file in the event that any data is already in it
        open(self.logfile, 'w').close()

        # Call the method to write something to the file
        self.install_log.step_complete()

        with open(self.logfile, "r") as logfile:
            logs = logfile.readlines()
            logfile.close()

        for line in logs:
            self.assertIn('Complete', line, msg="Log message was not properly written to the logfile.")


if __name__ == '__main__':
    unittest.main()
