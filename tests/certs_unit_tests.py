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
        self.cert_gen.generate_cert()

        # Ensure that the key file was created.
        assert os.path.exists(self.key_path + self.app_name + ".key") == 1

        # Ensure that the crt file was created.
        assert os.path.exists(self.cert_path + self.app_name + ".crt") == 1

    # def test_cert_exists(self):
    #     """Assume the certificate for the app_name has been generated, return True, otherwise return false"""
    #     # Test to check that the certificate from the previous test was generated.
    #     self.assertTrue(self.cert_gen.cert_exists())

    # def test_generate_custom_cert(self):
    #     """Create a custom cert 'bogus.crt'"""
    #     # Generate a custom certificate with the following values:
    #     keysize = 2048
    #     city = "Raleigh"
    #     state = "NC"
    #     loc = "US"
    #     org = "Bogus"
    #     orgunit = "Bogus"
    #     common_name = "www.bogus.com"
    #     encryption = "sha256"

    #     # Gen the Cert
    #     self.cert_gen.generate_custom_cert(keysize, city, state, loc, org, orgunit, common_name, encryption, "bogus.crt")

    #     # Ensure that the key file was created.
    #     assert os.path.exists(self.key_path + "bogus.key") == 1

    #     # Ensure that the crt file was created.
    #     assert os.path.exists(self.cert_path + "bogus.crt") == 1

    #     # Test faulty keysize
    #     keysize = "badkeysize"

    #     # Gen the Cert
    #     cert = self.cert_gen.generate_custom_cert(keysize, city, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
    #     cert_failure = cert.lines()
    #     for line in cert_failure:
    #         self.assertIn('Key Size must be a valid integer value', line, msg="A valid integer value was not passed in for keysize.")

    #     # Test faulty City
    #     keysize = 4096
    #     city = 1234

    #     # Gen the Cert
    #     cert = self.cert_gen.generate_custom_cert(keysize, city, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
    #     cert_failure = cert.lines()
    #     for line in cert_failure:
    #         self.assertIn('City must be a valid string value', line, msg="A valid string value was not passed in for city.")

    #     # Test faulty State
    #     city = "Raleigh"
    #     state = 1234

    #     # Gen the Cert
    #     cert = self.cert_gen.generate_custom_cert(keysize, city, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
    #     cert_failure = cert.lines()
    #     for line in cert_failure:
    #         self.assertIn('State must be a valid string value', line, msg="A valid string value was not passed in for state.")

    #     # Test faulty Location
    #     state = "NC"
    #     loc = 1234

    #     # Gen the Cert
    #     cert = self.cert_gen.generate_custom_cert(keysize, city, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
    #     cert_failure = cert.lines()
    #     for line in cert_failure:
    #         self.assertIn('Location must be a valid string value', line, msg="A valid string value was not passed in for loc.")

    #     # Test faulty Organization
    #     loc = "US"
    #     org = 1234

    #     # Gen the Cert
    #     cert = self.cert_gen.generate_custom_cert(keysize, city, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
    #     cert_failure = cert.lines()
    #     for line in cert_failure:
    #         self.assertIn('Organization must be a valid string value', line, msg="A valid string value was not passed in for org.")

    #     # Test faulty Organizational Unit
    #     org = "Bogus"
    #     orgunit = 1234

    #     # Gen the Cert
    #     cert = self.cert_gen.generate_custom_cert(keysize, city, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
    #     cert_failure = cert.lines()
    #     for line in cert_failure:
    #         self.assertIn('Organizational Unit must be a valid string value', line, msg="A valid string value was not passed in for orgunit.")

    #     # Test faulty Common Name
    #     orgunit = "Bogus"
    #     common_name = 1223

    #     # Gen the Cert
    #     cert = self.cert_gen.generate_custom_cert(keysize, city, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
    #     cert_failure = cert.lines()
    #     for line in cert_failure:
    #         self.assertIn('Common Name must be a valid string value', line, msg="A valid string value was not passed in for the common_name.")

    #     # Test faulty Encryption
    #     common_name = "www.bogus.com"
    #     encryption = 1234

    #     # Gen the Cert
    #     cert = self.cert_gen.generate_custom_cert(keysize, city, state, loc, org, orgunit, common_name, encryption, "bogusfail.crt")
    #     cert_failure = cert.lines()
    #     for line in cert_failure:
    #         self.assertIn('Encryption must be a valid string value', line, msg="A valid string value was not passed in for encryption.")

    # def test_alt_cert_exists(self):
    #     """Test the existance of a cert that was not auto generated"""
    #     # Test a certificate that does not yet exist.
    #     self.assertFalse(self.cert_gen.alt_cert_exists("void.crt"))

    #     # Test the custom cert we created in the previous test
    #     self.assertTrue(self.cert_gen.alt_cert_exists("bogus.crt"))

    # def test_validate_cert(self):
    #     """Validate the generic certificate created in an earlier test"""
    #     # Test the custom cert we created in the previous test
    #     self.assertTrue(self.cert_gen.validate_cert())

    #     # Test custom cert created in an earlier test
    #     self.assertTrue(self.cert_gen.validate_custom_cert("bogus.crt"))

    #     # Test a fail case
    #     self.assertFail(self.cert_gen.validate_custom_cert("void.crt"))

if __name__ == '__main__':
    unittest.main()
