# Dependencies : sudo apt install python3-dev python3-pip && sudo pip3 install wireless netifaces psutil
# Installation: sudo apt update && sudo apt --yes --force-yes install dnsmasq hostapd python3-dev python3-pip && sudo pip3 install pyaccesspoint

from PyAccessPoint import pyaccesspoint

access_point = pyaccesspoint.AccessPoint()