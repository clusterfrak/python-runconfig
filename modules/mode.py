"""
***************************************************************************
Class File:             Runconfig Mode Module
Authors/Maintainers:    Rich Nason (rnason@appcontainers.io)
Copyright:              Copyright 2016 Richard Nason
Description:            This class pull a Mode value from the containers
                        environment variables and will perform configuration
                        actions on the container based on the container's
                        mode setting.
***************************************************************************
"""
# *******************************************************************
# Required Modules:
# *******************************************************************
import os  # Used for various os level calls
from modules.globals import Globals
from modules.log import Log

# Instantiate the global variables.
GLOBALS = Globals()

# Instantiate the custom console logger.
INSTALL_LOG = Log()

# *******************************************************************
# Class Definitions:
# *******************************************************************


class Mode():
    """Class to configure the container mode"""

    def __init__(self):
        """Set instantiation variables"""
        # Create a list of packages that get installed
        if GLOBALS.is_rhel:
            self.package_mgr = "yum -y erase"
            self.remove_pkgs = self.package_mgr + " %s"
            self.mysql_pkg = "mysql-server"
        else:
            self.package_mgr = "apt-get -y remove --purge"
            self.remove_pkgs = self.package_mgr + " %s" + "; apt-get -y autoremove"
            self.mysql_pkg = "mysql-server-5.5"

    def config_verify(self, checkfile):
        """Method to determine if the environment has already been configured, Returns True/False value"""
        if os.path.isfile(checkfile):
            INSTALL_LOG.write_log_console("Existing $APPLICATION Instance detected...", "skipping...")
            return True
        else:
            return False

    def datavol(self, deplist):
        """Configure DataVol Mode"""
        # Log to console/logfile
        INSTALL_LOG.write_log_console("Data Volume Mode Detected...", "Removing unnecessary packages...")

        # Remove unnecessary packages, and recreate rpm/yum sync
        os.popen(self.remove_pkgs % (deplist,))
        os.popen(self.remove_pkgs % (self.mysql_pkg,))

        # Mark step complete
        INSTALL_LOG.step_complete()
