"""
APACHE CLASS:
Class that will handle all things associated with setting up and configuring the apache web service.
"""
# *******************************************************************
# Required Modules:
# *******************************************************************
# Import required modules
import os  # Used for various os level calls
from shutil import copyfile, move
from socket import gethostname  # Library used to gather the nodes hostname for the certificate

# Import custom modules
from modules.globals import Globals
from modules.log import Log

# Instantiate the global variables.
GLOBALS = Globals()

# Instantiate the custom console logger.
INSTALL_LOG = Log()

# *******************************************************************
# Class Definitions:
# *******************************************************************


class Apache():
    """Class to configure the apache"""

    def __init__(self):
        """Set instantiation variables"""
        self.app_name = os.environ['APP_NAME']

        # Create a list of packages that get installed
        if GLOBALS.is_rhel:
            self.package_mgr = "yum -y erase"
            self.apache_user = "apache"
            self.apache_group = "apache"
            self.apache_dir = "/etc/httpd/conf/"
            self.apache_app_dir = "/etc/httpd/conf.d/"
            self.apache_conf = "httpd.conf"
            self.apache_app_conf = "apache_cent.conf"
            self.apache_binary = "httpd"
            self.cert_path = "/etc/pki/tls/certs/"
            self.key_path = "/etc/pki/tls/private/"
            self.env_var_path = "/etc/sysconfig/httpd"
        else:
            self.package_mgr = "apt-get -y remove --purge"
            self.apache_user = "www-data"
            self.apache_group = "www-data"
            self.apache_dir = "/etc/apache2/"
            self.apache_app_dir = "/etc/apache2/sites-enabled/"
            self.apache_conf = "apache2.conf"
            self.apache_app_conf = "apache_deb.conf"
            self.apache_binary = "apache2"
            self.cert_path = "/etc/ssl/certs/"
            self.key_path = "/etc/ssl/private/"
            self.env_var_path = "/etc/apache2/envvars"

    def apache_init(self):
        """Method to configure the application if it has not been configured before"""
        INSTALL_LOG.write_log_console("Configuring Apache for the first time...", "")
        if not os.path.isdir("/var/www/html/" + self.app_name):
            os.makedirs("/var/www/html/" + self.app_name)
        try:
            with open("/var/www/html/" + self.app_name + "/index.php", "w+") as index:
                index.write("<?php phpinfo() ?>")
                index.close()
        except Exception as e:
            print("Could not create /var/www/html/" + self.app_name + "/index.php")
            print(e)

        # Mark step complete
        INSTALL_LOG.step_complete()

    def apache_config(self):
        """Configure Apache"""
        INSTALL_LOG.write_log_console("Configuring Apache config files...", "")

        # Backup the original File
        INSTALL_LOG.write_log("Backing up the Apache config file")
        copyfile(self.apache_dir + self.apache_conf, self.apache_dir + self.apache_conf + ".orig")

        # Backup the ssl.conf if it exists
        if os.path.isfile(self.apache_app_dir + "ssl.conf"):
            INSTALL_LOG.write_log("Disabling the default Apache ssl.conf file")
            move(self.apache_app_dir + "ssl.conf", self.apache_app_dir + "ssl.conf.backup")

        # Rename the application apache config file
        INSTALL_LOG.write_log("Renaming the Apache application config file")
        if os.path.isfile(self.apache_dir + "sites-available/" + self.apache_app_conf):
            move(self.apache_dir + "sites-available/" + self.apache_app_conf, self.apache_dir + "sites-available/" + self.app_name + ".conf")

        # Remove default configs if debian based distro
        if not GLOBALS.is_rhel:
            INSTALL_LOG.write_log("Disabling default debian based config files")
            if os.path.isfile(self.apache_app_dir + "000-default.conf"):
                os.unlink(self.apache_app_dir + "000-default.conf")
            INSTALL_LOG.write_log("Enabling the Apache application config")
            if not os.path.isfile(self.apache_app_dir + self.app_name + ".conf"):
                os.symlink(self.apache_dir + "sites-available/" + self.app_name + ".conf", self.apache_app_dir + self.app_name + ".conf")

        # Set the servername
        INSTALL_LOG.write_log("Setting server hostname in the Apache server config")
        # os.popen("sed -i 's/#ServerName\ www\.example\.com\:80/ServerName\ www\.'$APP_NAME'\:80/g")
        if GLOBALS.is_rhel:
            try:
                with open(self.apache_dir + self.apache_conf, "r") as apache_conf:
                    lines = apache_conf.readlines()
                with open(self.apache_dir + self.apache_conf, "w") as apache_conf:
                    for line in lines:
                        apache_conf.write(re.sub(r'^#ServerName www.example.com:80', 'ServerName www' + self.app_name + ':80', line))
                    apache_conf.close()
                    del lines
            except Exception as e:
                print("Could not open or write to " + self.apache_dir + self.apache_conf)
                print(e)
        else:
            try:
                with open(self.apache_dir + self.apache_conf, "a") as apache_conf:
                    apache_conf.write('ServerName www.' + self.app_name + ':80')
                    apache_conf.close()
            except Exception as e:
                print("Could not write to " + self.apache_dir + self.apache_conf)
                print(e)

        # Mark step complete
        INSTALL_LOG.step_complete()

    def apache_certs():
        # Modify the configs to use the certificate.
        INSTALL_LOG.write_log("Set certificate value in apache config file")

        # Change the apache config to use the the existing certificate.
        try:
            with open(self.apache_app_dir + self.app_name + ".conf", "r") as app_conf:
                lines = app_conf.readlines()
            with open(self.apache_app_dir + self.app_name + ".conf", "w") as app_conf:
                for line in lines:
                    app_conf.write(line.replace('localhost.crt', self.app_name + ".crt"))
                    app_conf.write(line.replace('localhost.key', self.app_name + "."))
                    app_conf.write(re.sub(r'^localhost.crt', self.app_name + ".crt", line))
                    app_conf.write(re.sub(r'^localhost.key', self.app_name + ".key", line))
                app_conf.close()
                del lines
        except Exception as e:
            print("Could not read or write to " + self.apache_app_dir + self.app_name)
            print(e)

        # Mark step complete
        INSTALL_LOG.step_complete()

    def apache_envvars(self):
        """Configure Apache Environment Varaiables"""
        INSTALL_LOG.write_log_console("Setting Apache variables to allow", "variable substitution in the apache config")

        INSTALL_LOG.write_log("Writing apache variables to " + self.env_var_path)
        try:
            with open(self.env_var_path, "a") as envars:
                envars.write("\n\n")
                envars.write("# Set Apache Environment Variables that will be passed to Apache via /etc/sysconfig/httpd/PassEnv\n")
                envars.write("# Must have a2enmod env enabled\n\n")
                envars.write("APP=\"" + self.app_name + "\"\n")
                envars.write("SVRALIAS=\"" + os.environ['APACHE_SVRALIAS'] + "\"\n")
                envars.write("HOSTNAME=" + gethostname() + "\n\n")

                INSTALL_LOG.write_log("Exporting Apache Variables to " + self.env_var_path)
                envars.write("# Export the variables to sysconfig/PassEnv\n")
                envars.write("export APP SVRALIAS HOSTNAME\n")
                envars.close()
        except Exception as e:
            print("Could not write to " + self.env_var_path)
            print(e)

        # Mark step complete
        INSTALL_LOG.step_complete()

    def apache_start(self):
        """Start Apache Web Services"""
        INSTALL_LOG.write_log_console("Staring Apache Web Services...", "")

        # Add the service start to the bashrc file.
        try:
            with open("/root/.bashrc", "a") as bashrc:
                bashrc.write("service " + self.apache_binary + " start")
                bashrc.close()
        except Exception as e:
            print("Could not modify the root bashrc file")
            print(e)

        # Start Apache.
        start_process = os.popen("service " + self.apache_binary + " start")
        output = start_process.readline()
        print(output)
        start_process.close()

        # Mark step complete
        INSTALL_LOG.step_complete()
