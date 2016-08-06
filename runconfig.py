"""Runconfig Main Module"""
import os  # Used for various os level calls

# Import custom modules
from modules.globals import Globals
from modules.log import Log
from modules.mode import Mode

# Import the application modules
from modules.apache import Apache

# Instantiate the global variables.
GLOBALS = Globals()

# Instantiate the custom console logger.
INSTALL_LOG = Log()

#####################################################################
# ***********************  OS Env Variables  ***********************
#####################################################################

# Get Environment variables passed in by the Docker run statement
APP_NAME = os.environ['APP_NAME']
MODE = os.environ['MODE']
MODE = MODE.upper()

#####################################################################
# *************************  MODIFY VALUES  *************************
#####################################################################

# Script Variables...
# Full name of the application that this file will configured (Wordpress/MediaWiki/etc..)
APPLICATION = "Apache"

# File that the script will check to see if the application is already configured.
CHECKFILE = "index.php"
CHECKFILE_PATH = "/var/www/html/"

# Full path to the file that the script will check if the application has already been configured.
CHECKFILE_PATH = os.path.join(CHECKFILE_PATH + APP_NAME + "/", CHECKFILE)

# APPVER will correspond to the APPLICATION VERSION such as WIKIVER or master.zip.
# Its the file that gets dumped in /var/www/html and gets moved to /var/www/html/APP_NAME
APPVER = ""

# Deplist conatins a list of all of the packages that are installed, that will be uninstalled if the container is ran in storage mode.
CENT_DEPLIST = "httpd mod_rewrite mod_ssl mod_env php php-common php-cli php-mysql php-pgsql php-xml php-pdo php-xcache xcache-admin php-intl ImageMagick"
DEB_DEPLIST = "apache2 php5 php5-cli php5-common php5-mysql php5-xmlrpc imagemagick php5-pgsql"


#####################################################################
# ***********************  VARAIABLE VALUES  ***********************
#####################################################################

# Create a list of packages that get installed
if GLOBALS.is_rhel:
    DEPLIST = CENT_DEPLIST
else:
    DEPLIST = DEB_DEPLIST

##################################################################
# ***********************  CONFIGURE MODE  ***********************
##################################################################
app_mode = Mode()

if "DATAVOL" in MODE:
    app_mode.datavol(DEPLIST)
else:
    # Check to see if the environment has already been configured
    CONFIGURED = app_mode.config_verify(CHECKFILE_PATH)

##################################################################
# ***********************  CONFIGURE APP  ***********************
##################################################################
# Instantiate the Application Module
configuration = Apache()

if not CONFIGURED:
    # Configure apache
    configuration.apache_config()
    # Generate Certificates
    configuration.apache_certs()
    # Create the php.info page
    configuration.apache_init()

# Set Apache Envars
configuration.apache_envvars()

# Start Apache
configuration.apache_start()

# Remove config scripts
INSTALL_LOG.write_log_console("Removing configuration scripts", "")
os.popen("sed -i '/\/tmp\/.\/.runconfig.py/d' /root/.bashrc")

# Mark step complete
INSTALL_LOG.step_complete()
