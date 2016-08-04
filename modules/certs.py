"""
***************************************************************************
Class File:             Runconfig Cert Generation Module
Authors/Maintainers:    Rich Nason (rnason@appcontainers.io)
Copyright:              Copyright 2016 Richard Nason
Description:            This class will provide the ability to generate a self
                        signed certificate that will be configured and used for
                        the container services.
***************************************************************************
"""
# *******************************************************************
# Required Modules:
# *******************************************************************
import os  # Used for various os level calls
import datetime  # Used for timestamp
# pyOpenSSL requires libffi-dev, libssl-dev, and a pip install of pyOpenSSL
from OpenSSL import crypto, SSL  # pylint: disable=unused-import

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


class CertGen():
    """Class to handle all things certficate related"""

    def __init__(self):
         """Set instantiation variables"""
        self.app_name = os.environ['APP_NAME']

        if GLOBALS.is_rhel:
            self.cert_path = "/etc/pki/tls/certs/"
            self.key_path = "/etc/pki/tls/private/"
            self.env_var_path = "/etc/sysconfig/httpd"
        else:
            self.cert_path = "/etc/ssl/certs/"
            self.key_path = "/etc/ssl/private/"
            self.env_var_path = "/etc/apache2/envvars"

    def cert_exists(self):
        """Check to see if a certificate already exists, returns true if it exists, false if not"""
        if os.path.isfile(self.cert_path + self.app_name + ".crt"):
            INSTALL_LOG.write_log_console("Existing application certificate detected...", "Skipping...")
            return True
        else:
            return False

    def alt_cert_exists(self, cert_name):
        """Check to see if a certificate already exists, returns true if it exists, false if not"""
        if os.path.isfile(self.cert_path + cert_name):
            INSTALL_LOG.write_log_console("Existing application certificate detected...", "Skipping...")
            return True
        else:
            return False

    def generate_cert(self):
        """Generate Self Signed Certificates"""
        INSTALL_LOG.write_log_console("Generate SSL Cert...", "")
        
        # Generate the Cert Private Key
        INSTALL_LOG.write_log("Generating SSL Key....")
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)

        # Generate the Certifcate using the generated private Key good for 10 years.
        cert = crypto.X509()
        cert.get_subject().C = "US"
        cert.get_subject().ST = "One of them"
        cert.get_subject().L = "US"
        cert.get_subject().O = self.app_name
        cert.get_subject().OU = self.app_name
        cert.get_subject().CN = gethostname()
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(315360000)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha512')

        # Write the cert files to disk
        open(self.cert_path + self.app_name + ".crt", "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(self.key_path + self.app_name + ".key", "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    def generate_custom_cert(self, keysize, city, state, loc, org, orgunit, common_name, encryption, cert_name):
        """Generate Custom Self Signed Certificates"""
        INSTALL_LOG.write_log_console("Generate Custom SSL Cert...", "")

        OK = True
        
        # Make sure that the passed in values are legit
        if not isinstance(keysize, int):
            OK = False

        if keysize > 4096:
            print("Passed keysize can not be used for sha2 certificate, and could be marked invalid in some browsers.\n")
            print("A keysize of at least 4096 is recommended.\n")

        if city == "" or city == None or not isinstance(city, string):
            OK = False

        if state == "" or state == None or not isinstance(state, string):
            OK = False

        if loc == "" or loc == None or not isinstance(loc, string):
            OK = False

        if org == "" or org == None or not isinstance(org, string):
            OK = False

        if orgunit == "" or orgunit == None or not isinstance(orgunit, string):
            OK = False

        if common_name == "" or common_name == None or not isinstance(common_name, string):
            OK = False

        if encryption == "" or encryption == None or not isinstance(encryption, string):
            OK = False

        if encryption != 'sha512':
            print("Passed encrytion can not be used for sha2 certificate, and could be marked invalid in some browsers.\n")
            print("An encryption level of at least sha512 is recommended.\n")

        
        # Generate the Cert Private Key
        INSTALL_LOG.write_log("Generating SSL Key....")
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, keysize)

        # Generate the Certifcate using the generated private Key good for 10 years.
        cert = crypto.X509()
        cert.get_subject().C = city
        cert.get_subject().ST = state
        cert.get_subject().L = loc
        cert.get_subject().O = org
        cert.get_subject().OU = orgunit
        cert.get_subject().CN = common_name
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(315360000)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, encryption)

        # Write the cert files to disk
        open(self.cert_path + cert_name, "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(self.key_path + cert_name + ".key", "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))


    # TODO:
    # Add to trusted cert store
    # Validate certificate is or is not trusted.