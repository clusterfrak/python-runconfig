"""Runconfig Logging Module"""
import os  # Used for various os level calls
import datetime  # Used for timestamp


class Log():
    """This module will handle logging config info to the console and to the logfile"""

    def __init__(self):
        """Set instantiation variables"""
        self.log_file = "/tmp/install.log"
        if not os.path.isfile(self.log_file):
            os.makedirs(self.log_file)

    def write_log(self, msg):
        """Write sent message to logfile"""
        with open(self.log_file, 'w') as log:
            log.write(datetime.datetime.now() + ": " + msg + "\n")
            log.close()

    def write_console(self, msg1, msg2):
        """Write the sent messages to the console"""
        print("\n")
        print("**************************************************")
        print("* " + msg1)
        print("* " + msg2)
        print("**************************************************")
        print("\n")

    def log_console(self, msg1, msg2):
        """Write the sent messages to the logfile"""
        with open(self.log_file, 'w') as log:
            log.write("\n")
            log.write("**************************************************")
            log.write("* " + datetime.datetime.now() + ": " + msg1)
            log.write("* " + datetime.datetime.now() + ": " + msg2)
            log.write("**************************************************")
            log.write("\n")
            log.close()

    def step_complete(self):
        """Echo that the step has completed."""
        with open(self.log_file, 'w') as log:
            print("Complete")
            log.write(datetime.datetime.now() + ": Step Complete\n")
            log.close()
