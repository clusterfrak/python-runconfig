"""Module to configure the container mode"""
# Import custom modules
import os  # Used to verify the checkfile
from modules.log import Log

# Instantiate the custom console logger.
config_logger = Log()


class Mode(DEPLIST):
    """Class to configure the container mode"""

     def __init__(self):
         """Set instantiation variables"""
         # Get the OS version
         self.rhel_distro = False
         if os.path.isfile('/etc/redhat-release'):
            self.rhel_distro = True

          # Create a list of packages that get installed
          if rhel_distro:
              self.package_mgr = "yum -y erase"
              self.deplist = DEPLIST
              self.mysql_pkg = "mysql-server"
              self.remove_pkgs = self.package_mgr + " " + self.deplist
          else:
              self.package_mgr = "apt-get -y remove --purge"
              self.deplist = DEPLIST
              self.mysql_pkg = "mysql-server-5.5"
              self.remove_pkgs = self.package_mgr + " " + self.deplist + "; apt-get -y autoremove"

     def config_verif(self, checkfile):
          """Method to determine if the environment has already been configured, Returns True/False value"""
          if os.path.isfile(checkfile):
               config_logger.write_console("Existing $APPLICATION Instance detected..." "skipping...")
               config_logger.write_console("Existing $APPLICATION Instance detected..." "skipping...")
               return True
          else:
               return False

     def datavol(self):
          """Configure DataVol Mode"""
          # Log to console/logfile
          config_logger.write_console("Data Volume Mode Detected...", "Removing unnecessary packages...")
          config_logger.log_console("Data Volume Mode Detected...", "Removing unnecessary packages...")

          # Remove unnecessary packages without yanking apache, and recreate rpm/yum sync
          os.popen(self.remove_pkgs)

          # Mark step complete
          config_logger.step_complete()


