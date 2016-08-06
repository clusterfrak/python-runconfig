"""
***************************************************************************
Unit Test:              Runconfig Cert Generation Module Unit Tests
Authors/Maintainers:    Rich Nason (rnason@appcontainers.io)
Copyright:              Copyright 2016 Richard Nason
Description:            These Unit tests will tests the CertGen Class to ensure proper code level functionality.
***************************************************************************
"""
# *******************************************************************
# Required Modules:
# *******************************************************************
import unittest
import os
from modules.globals import Globals
from modules.certs import CertGen


class CertTests(unittest.TestCase):
    """Tests for certs.py"""

    def setUp(self):
        """Initialize the class, and instantiate a CertGen instance"""
        self.global_variables = Globals()
        self.cert_gen = CertGen()

        """Set instantiation variables"""
        self.app_name = os.environ['APP_NAME']

        if self.app_name == "" or self.app_name is None:
            self.app_name = "Test.com"

        if self.global_variables.is_rhel():
            self.cert_path = "/etc/pki/tls/certs/"
            self.key_path = "/etc/pki/tls/private/"
        else:
            self.cert_path = "/etc/ssl/certs/"
            self.key_path = "/etc/ssl/private/"

    def test_generate_cert(self):
        """Generate a certificate and ensure that the cert key and crt file were generated."""
        # Generate a generic certificate:
        print("Generating Generic Cert...")
        self.cert_gen.generate_cert()

        # Ensure that the key file was created.
        print("Validating generic key file was created...")
        assert os.path.exists(self.key_path + self.app_name + ".key") == 1

        # Ensure that the crt file was created.
        print("Validating generic cert file was created...")
        assert os.path.exists(self.cert_path + self.app_name + ".crt") == 1

        """Assume the certificate for the app_name has been generated, return True, otherwise return false"""
        # Test to check that the certificate from the previous test was generated.
        print("Validating that the Generic certificate exists...")
        self.assertTrue(self.cert_gen.cert_exists())

    def test_generate_custom_cert(self):
        """Create a custom cert 'bogus.crt'"""
        # Generate a custom certificate with the following values:
        print("Generating custom certificate key pair...")
        keysize = 2048
        country = "US"
        state = "NC"
        loc = "Raleigh"
        org = "Bogus"
        orgunit = "Bogus"
        common_name = "www.bogus.com"
        encryption = "sha256"

        # Gen the Cert
        self.cert_gen.generate_custom_cert(keysize, country, state, loc, org, orgunit, common_name, encryption, "bogus.crt")

        # Ensure that the key file was created.
        print("Validating custom key file was created...")
        assert os.path.exists(self.key_path + "bogus.key") == 1

        # Ensure that the crt file was created.
        print("Validating custom cert file was created...")
        assert os.path.exists(self.cert_path + "bogus.crt") == 1

        print("Testing faulty values...")
        # Test faulty keysize
        keysize = "badkeysize"

        # Gen the Cert
        cert = self.cert_gen.generate_custom_cert(keysize, country, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
        self.assertIn('Key Size must be a valid integer value', cert, msg="A valid integer value was not passed in for keysize.")

        # Test faulty country
        keysize = 4096
        country = 1234

        # Gen the Cert
        cert = self.cert_gen.generate_custom_cert(keysize, country, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
        self.assertIn('Country must be a valid string value', cert, msg="A valid string value was not passed in for country.")

        # Test faulty State
        country = "US"
        state = 1234

        # Gen the Cert
        cert = self.cert_gen.generate_custom_cert(keysize, country, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
        self.assertIn('State must be a valid string value', cert, msg="A valid string value was not passed in for state.")

        # Test faulty Location
        state = "NC"
        loc = 1234

        # Gen the Cert
        cert = self.cert_gen.generate_custom_cert(keysize, country, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
        self.assertIn('Location must be a valid string value', cert, msg="A valid string value was not passed in for loc.")

        # Test faulty Organization
        loc = "Raleigh"
        org = 1234

        # Gen the Cert
        cert = self.cert_gen.generate_custom_cert(keysize, country, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
        self.assertIn('Organization must be a valid string value', cert, msg="A valid string value was not passed in for org.")

        # Test faulty Organizational Unit
        org = "Bogus"
        orgunit = 1234

        # Gen the Cert
        cert = self.cert_gen.generate_custom_cert(keysize, country, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
        self.assertIn('Organizational Unit must be a valid string value', cert, msg="A valid string value was not passed in for orgunit.")

        # Test faulty Common Name
        orgunit = "Bogus"
        common_name = 1223

        # Gen the Cert
        cert = self.cert_gen.generate_custom_cert(keysize, country, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
        self.assertIn('Common Name must be a valid string value', cert, msg="A valid string value was not passed in for the common_name.")

        # Test faulty Encryption
        common_name = "www.bogus.com"
        encryption = 1234

        # Gen the Cert
        cert = self.cert_gen.generate_custom_cert(keysize, country, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
        self.assertIn('Encryption must be a valid encrytion value such as sha256 or sha512', cert, msg="A valid string value was not passed in for encryption.")

        """Test the existance of a cert that was not auto generated"""
        # Test a certificate that does not yet exist.
        print("Validating custom cert exists failure...")
        self.assertFalse(self.cert_gen.custom_cert_exists("void.crt"))

        # Test the custom cert we created in the previous test
        print("Validating custom cert exists success...")
        self.assertTrue(self.cert_gen.custom_cert_exists("bogus.crt"))

    def tearDown(self):
        """Perform file cleanup from tests"""
        if os.path.isfile(self.cert_path + self.app_name + ".crt"):
            os.remove(self.cert_path + self.app_name + ".crt")
        if os.path.isfile(self.key_path + self.app_name + ".key"):
            os.remove(self.key_path + self.app_name + ".key")
        if os.path.isfile(self.cert_path + "bogus.crt"):
            os.remove(self.cert_path + "bogus.crt")
        if os.path.isfile(self.key_path + "bogus.key"):
            os.remove(self.key_path + "bogus.key")

if __name__ == '__main__':
    unittest.main()
