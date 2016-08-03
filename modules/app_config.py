"""Module to configure various container applications"""
# Import required modules
import os  # Used for various os level calls
import re  # Used for word substitiution
from shutil import copyfile, move
from OpenSSL import crypto, SSL  # pylint: disable=unused-import
from socket import gethostname  # Library used to gather the nodes hostname for the certificate

# Import custom modules
from modules.log import Log

# Instantiate the custom console logger.
config_logger = Log()


class Apache():
    """Class to configure the apache"""

    def __init__(self):
        """Set instantiation variables"""
        # Get the OS version
        self.rhel_distro = False
        if os.path.isfile('/etc/redhat-release'):
            self.rhel_distro = True

        self.app_name = os.environ['APP_NAME']

        # Create a list of packages that get installed
        if self.rhel_distro:
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
            self.mysql_pkg = "mysql-server"
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
            self.mysql_pkg = "mysql-server-5.5"

    def apache_init(self):
        """Method to configure the application if it has not been configured before"""
        config_logger.write_console("Configuring Apache for the first time..." "")
        config_logger.log_console("Configuring Apache for the first time..." "")
        os.makedirs("/var/www/html/" + self.app_name)
        with open("/var/www/html/" + self.app_name + "/index.php") as index:
            index.write("<?php phpinfo() ?>")
            index.close()
        # Mark step complete
        config_logger.step_complete()

    def apache_config(self):
        """Configure Apache"""
        config_logger.write_console("Configuring Apache config files..." "")
        config_logger.log_console("Configuring Apache config files..." "")

        # Backup the original File
        config_logger.write_log("Backing up the Apache config file")
        copyfile(self.apache_dir + self.apache_conf, self.apache_dir + self.apache_conf + ".orig")

        # Backup the ssl.conf if it exists
        if os.path.isfile(self.apache_app_dir + "ssl.conf"):
            config_logger.write_log("Disabling the default Apache ssl.conf file")
            move(self.apache_app_dir + "ssl.conf", self.apache_app_dir + "ssl.conf.backup")

        # Rename the application apache config file
        config_logger.write_log("Renaming the Apache application config file")
        move(self.apache_app_dir + self.apache_app_conf, self.apache_app_dir + self.app_name + ".conf")

        # Remove default configs if debian based distro
        if not self.rhel_distro:
            config_logger.write_log("Disabling default debian based config files")
            os.remove(self.apache_app_dir + "/*")
            config_logger.write_log("Enabling the Apache application config")
            os.symlink(self.apache_dir + "sites-available/" + self.app_name + ".conf", self.apache_app_dir + self.app_name + ".conf")

        # Set the servername
        config_logger.write_log("Setting server hostname in the Apache server config")
        # os.popen("sed -i 's/#ServerName\ www\.example\.com\:80/ServerName\ www\.'$APP_NAME'\:80/g")
        if self.rhel_distro:
            with open(self.apache_dir + self.apache_conf, "r") as apache_conf:
                lines = apache_conf.readlines()
            with open(self.apache_dir + self.apache_conf, "w") as apache_conf:
                for line in lines:
                    apache_conf.write(re.sub(r'^#ServerName www.example.com:80', 'ServerName www' + self.app_name + ':80', line))
        else:
            with open(self.apache_dir + self.apache_conf, "a") as apache_conf:
                apache_conf.write('ServerName www.' + self.app_name + ':80')

        # Mark step complete
        config_logger.step_complete()

    def apache_certs(self):
        """Generate Apache Self Signed Certificates"""
        # Check to see if a certificate already exists
        if os.path.isfile(self.cert_path + "/" + self.app_name + ".crt"):
            config_logger.write_console("Existing application certificate detected..." "Skipping...")
            config_logger.write_log("Existing application certificate detected..." "Skipping...")

        # If an existing certificate was not found, then generate one for the app.
        else:
            config_logger.write_console("Generate SSL Cert and Configure Apache..." "")
            config_logger.write_log("Generate SSL Cert and Configure Apache..." "")

            config_logger.write_log("Generating SSL Key....")

            # Create a key pair
            k = crypto.PKey()
            k.generate_key(crypto.TYPE_RSA, 2048)

            # Create a self-signed cert good for 10 years
            cert = crypto.X509()
            cert.get_subject().C = "US"
            cert.get_subject().ST = "One of the 50"
            cert.get_subject().L = ""
            cert.get_subject().O = self.app_name
            cert.get_subject().OU = ""
            cert.get_subject().CN = gethostname()
            cert.set_serial_number(1000)
            cert.gmtime_adj_notBefore(0)
            cert.gmtime_adj_notAfter(315360000)
            cert.set_issuer(cert.get_subject())
            cert.set_pubkey(k)
            cert.sign(k, 'sha256')

            # Write the cert files to disk
            open(self.cert_path + self.app_name + ".crt", "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
            open(self.key_path + self.app_name + ".key", "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

        # Modify the configs to use the certificate.
        config_logger.write_log("Set certificate value in apache config file")

        # Change the apache config to use the the existing certificate.
        with open(self.apache_app_dir + self.apache_app_conf, "r") as app_conf:
            lines = app_conf.readlines()
        with open(self.apache_app_dir + self.apache_app_conf, "w") as app_conf:
            for line in lines:
                app_conf.write(re.sub(r'^localhost.crt', self.app_name + ".crt", line))
                app_conf.write(re.sub(r'^localhost.key', self.app_name + ".key", line))

        # Mark step complete
        config_logger.step_complete()

    def apache_envvars(self):
        """Configure Apache Environment Varaiables"""
        config_logger.write_console("Setting Apache variables to allow" "variable substitution in the apache config")
        config_logger.write_log("Setting Apache variables to allow" "variable substitution in the apache config")

        config_logger.write_log("Writing apache variables to " + self.env_var_path)
        with open(self.env_var_path, "w") as envars:
            envars.write("# Set Apache Environment Variables that will be passed to Apache via /etc/sysconfig/httpd/PassEnv (Must have a2enmod env enabled")
            envars.write("APP=" + self.app_name)
            envars.write("SVRALIAS=" + os.environ['APACHE_SVRALIAS'])
            envars.write("HOSTNAME=" + gethostname())

            config_logger.write_log("Exporting Apache Variables to " + self.env_var_path)
            envars.write("# Export the variables to sysconfig/PassEnv")
            envars.write("export APP SVRALIAS HOSTNAME\n")

    def apache_start(self):
        """Start Apache Web Services"""
        config_logger.write_console("Staring Apache Web Services...")
        config_logger.write_log("Staring Apache Web Services...")

        with open("/root/.bashrc", "a") as bashrc:
            bashrc.write("service " + self.apache_binary + " start")

        os.popen("service " + self.apache_binary + " start")

        # Mark step complete
        config_logger.step_complete()
