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

    def tearDown(self):
        """Perform file cleanup from tests"""
        if os.path.isfile("/var/www/html/" + self.app_name + "/index.php"):
            os.remove("/var/www/html/" + self.app_name + "/index.php")

        # Move the original apache config back
        if os.path.isfile(self.apache_dir + self.apache_conf + ".orig"):
            move(self.apache_dir + self.apache_conf + ".orig", self.apache_dir + self.apache_conf)

if __name__ == '__main__':
    unittest.main()
