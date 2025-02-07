"""
cip_objects.py file

This file defines a class with appropriate parameters and unique identifiers 
to configure each component within IO Map to it's corresponding physical hardware. 

Overview:
1. Define a class with appropriate parameters to connect to physical hardware

"""

# Define a class to handle the hub component
class PhidgetSBC4:
    def __init__(self, uid: str, host: str) -> None: # Necessary parameters include the IP Address and Host
        self.uniqueId = uid
        self.host = host
        