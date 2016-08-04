"""
***************************************************************************
Class File:             Runconfig Globals Module
Authors/Maintainers:    Rich Nason (rnason@appcontainers.io)
Copyright:              Copyright 2016 Richard Nason
Description:            Singleton Class that will handle global variable used throught all other classes.
***************************************************************************
"""
# *******************************************************************
# Required Modules:
# *******************************************************************
import os  # Make System Calls to interact with host

# *******************************************************************
# Class Definitions:
# *******************************************************************


class Globals:
    """Singleton class that handles global variables."""

    class State:
        """Singleton class for global variables."""

        def __init__(self):
            """Initialize the State sub class"""
            # Check to see if the container is a RHEL based distro.
            if os.path.isfile('/etc/redhat-release'):
                self.rhel_distro = True
            else:
                self.rhel_distro = False

        def is_rhel(self):
            """If the container is rhel based, return bool value defining if rhel based or not"""
            return self.rhel_distro

    instance = None

    def __init__(self):
        """Init Globals"""
        if Globals.instance is None:
            Globals.instance = Globals.State()

    def is_rhel(self):
        """If the container is rhel based, return bool value defining if rhel based or not"""
        return Globals.instance.is_rhel()

    def __getattr__(self, name):
        """Get Attributes"""
        return getattr(self.instance, name)
