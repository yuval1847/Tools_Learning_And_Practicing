import argparse
from Techniques_Enum import Techniques

# An object which can read flags when the script start to run
parser = argparse.ArgumentParser(description="A basic port scanner that yuyu1847 has been created!")

# Flags of the script
parser.add_argument("--ip", type=str, action="store", help="The target's IPv4 address")
parser.add_argument("--ports", type=str, action="store", help="ports to scan")
parser.add_argument("--scanning_technics", type=Techniques, choices=list(Techniques), action="store", help="The type of the scanning technics")

# Parse arguments which contains all the parsed values
args = parser.parse_args()