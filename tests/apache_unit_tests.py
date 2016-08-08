"""
***************************************************************************
Unit Test:              Runconfig Apache Configuration Module Unit Tests
Authors/Maintainers:    Rich Nason (rnason@appcontainers.io)
Copyright:              Copyright 2016 Richard Nason
Description:            These Unit tests will tests the Apache Class to ensure proper code level functionality.
***************************************************************************
"""
# *******************************************************************
# Required Modules:
# *******************************************************************
import unittest
import os
from shutil import copyfile, move
from modules.globals import Globals
from modules.apache import Apache


class ApacheTests(unittest.TestCase):
    """Tests for apache.py"""

    def setUp(self):
        """Initialize the class, and instantiate a CertGen instance"""
        self.global_variables = Globals()
        self.apache = Apache()

        """Set instantiation variables"""
        self.app_name = os.environ['APP_NAME']

        if self.app_name == "" or self.app_name is None:
            self.app_name = "Test.com"

        if self.global_variables.is_rhel():
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
            self.cert_path = "/etc/pki/tls/certs/"
            self.key_path = "/etc/pki/tls/private/"

    def test_apache_init(self):
        """Generate the php info page and test the file was created properly"""
        self.apache.apache_init()

        # Ensure that the key file was created.
        assert os.path.exists("/var/www/html/" + self.app_name + "/index.php") == 1

    def test_apache_config(self):
        """Test the backup and modification to the main apache server conf'"""
        self.apache.apache_config()

        # Test to make sure that the config file was backed up
        assert os.path.exists(self.apache_dir + self.apache_conf + ".orig") == 1

        # Test to ensure that the ServerName was written properly to the file
        servername_set = False
        with open(self.apache_dir + self.apache_conf, "r") as apache_conf:
            config = apache_conf.readlines()
            apache_conf.close()
        for line in config:
            if "ServerName www." + self.app_name + ":80" in line:
                servername_set = True
        self.assertTrue(servername_set)

    def test_apache_app_config(self):
        """Test the backup and modification to the main apache application conf'"""
        self.apache.apache_app_config()

        # Test to make sure that the ssl config file was moved
        assert os.path.exists(self.apache_app_dir + "ssl.conf") == 0

        if self.global_variables.is_rhel():
            assert os.path.exists(self.apache_app_dir + "ssl.conf.disabled") == 1

        # Test to ensure that the application apache config file was renamed properly.
        assert os.path.exists(self.apache_dir + "sites-available/" + self.apache_app_conf) == 0
        assert os.path.exists(self.apache_dir + "sites-available/" + self.app_name + ".conf") == 1

        # If debian, make sure that default configs were or removed.
        if not self.global_variables.is_rhel():
            assert os.path.exists(self.apache_app_dir + "000-default.conf") == 0
            assert os.path.exists(self.apache_app_dir + self.app_name + ".conf") == 1

    def tearDown(self):
        """Perform file cleanup from tests"""
        if os.path.isfile("/var/www/html/" + self.app_name + "/index.php"):
            os.remove("/var/www/html/" + self.app_name + "/index.php")

        # Move the original apache config back
        if os.path.isfile(self.apache_dir + self.apache_conf + ".orig"):
            move(self.apache_dir + self.apache_conf + ".orig", self.apache_dir + self.apache_conf)

        # Move the SSL file back
        if os.path.isfile(self.apache_app_dir + "ssl.conf.disabled"):
            move(self.apache_app_dir + "ssl.conf.disabled", self.apache_app_dir + "ssl.conf")

        # Rename the Application file back to its original name
        if os.path.isfile(self.apache_dir + "sites-available/" + self.app_name + ".conf"):
            os.unlink(self.apache_app_dir + self.app_name + ".conf")
            move(self.apache_dir + "sites-available/" + self.app_name + ".conf", self.apache_dir + "sites-available/" + self.apache_app_conf)

        # If debian, put the symlinks back to the way they originally were.
        if not self.global_variables.is_rhel():
            print("searching for " + self.apache_app_dir + self.app_name + ".conf")
            if os.path.exists(self.apache_app_dir + self.app_name + ".conf"):
                os.remove(self.apache_app_dir + self.app_name + ".conf")
            if not os.path.exists(self.apache_app_dir + "000-default.conf"):
                os.symlink(self.apache_dir + "sites-available/000-default.conf", self.apache_app_dir + "000-default.conf")

if __name__ == '__main__':
    unittest.main()
