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
from socket import gethostname  # Library used to gather the nodes hostname for the certificate

# pyOpenSSL requires libffi-dev, libssl-dev, and a pip install of pyOpenSSL, and pycrypto
from OpenSSL import crypto, SSL  # pylint: disable=unused-import
from Crypto.Util import asn1  # Used to validate the self signed certificate

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

        if GLOBALS.is_rhel():
            self.cert_path = "/etc/pki/tls/certs/"
            self.key_path = "/etc/pki/tls/private/"
        else:
            self.cert_path = "/etc/ssl/certs/"
            self.key_path = "/etc/ssl/private/"

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
        """Generate Generic Self Signed Certificates"""
        self.generate_custom_cert(4096, "US", "One of the 50", "US", self.app_name, self.app_name, gethostname(), "sha512", self.app_name + ".crt")

    def generate_custom_cert(self, keysize, city, state, loc, org, orgunit, common_name, encryption, cert_name):
        """Generate Custom Self Signed Certificates"""
        INSTALL_LOG.write_log_console("Generate Custom SSL Cert...", "")

        valid = True

        # Make sure that the passed in values are legit
        if not isinstance(keysize, int):
            print("Key Size must be a valid integer value")
            valid = False

        if keysize > 4096:
            print("Passed keysize can not be used for sha2 certificate, and could be marked invalid in some browsers.\n")
            print("A keysize of at least 4096 is recommended.\n")

        if city == "" or city is None or not isinstance(city, str):
            print("City must be a valid string value")
            valid = False

        if state == "" or state is None or not isinstance(state, str):
            print("State must be a valid string value")
            valid = False

        if loc == "" or loc is None or not isinstance(loc, str):
            print("Location must be a valid string value")
            valid = False

        if org == "" or org is None or not isinstance(org, str):
            print("Org must be a valid string value")
            valid = False

        if orgunit == "" or orgunit is None or not isinstance(orgunit, str):
            print("Organizaional Unit must be a valid string value")
            valid = False

        if common_name == "" or common_name is None or not isinstance(common_name, str):
            print("Common Name must be a valid string value")
            valid = False

        if encryption == "" or encryption is None or not isinstance(encryption, str):
            print("Encryption must be a valid encrytion value such as sha512")
            valid = False

        if encryption != 'sha512':
            print("Passed encrytion can not be used for sha2 certificate, and could be marked invalid in some browsers.\n")
            print("An encryption level of at least sha512 is recommended.\n")

        # Generate the Cert Private Key
        if valid:
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

            # Define key name
            key_name = cert_name.replace(".crt", ".key")

            # Write the cert files to disk
            open(self.cert_path + cert_name, "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
            open(self.key_path + key_name, "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
        else:
            print("Invalid values were passed into the create certificate process, as a result the certificate can not be generated at this time\n")
            print("Please check your values, and try again.")

    def validate_cert(self):
        """Method to valdiate a certificate with its public key"""
        validation = self.validate_custom_cert(self.cert_path + self.app_name + ".crt", self.key_path + self.app_name + ".key")
        return validation

    def validate_custom_cert(self, cert_name, key_name):
        """Method to valdiate a certificate with its public key"""
        # Define the location of the certificate
        cert = cert_name

        # Define the location of the key
        priv = key_name

        pub = cert.get_pubkey()

        # Only works for RSA
        # if pub.type()! = crypto.TYPE_RSA or priv.type()! = crypto.TYPE_RSA:
        #    raise Exception('Validation currently only works on RSA Type Key/Cert Pairs')

        # Set cert/key pair for validation
        pub_asn1 = crypto.dump_privatekey(crypto.FILETYPE_ASN1, pub)
        priv_asn1 = crypto.dump_privatekey(crypto.FILETYPE_ASN1, priv)

        # Decode DER
        pub_der = asn1.DerSequence()
        pub_der.decode(pub_asn1)
        priv_der = asn1.DerSequence()
        priv_der.decode(priv_asn1)

        # Get the modulus
        pub_modulus = pub_der[1]
        priv_modulus = priv_der[1]

        if pub_modulus == priv_modulus:
            return True
        else:
            return False
