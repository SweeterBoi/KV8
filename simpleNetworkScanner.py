'''
This script defines functions utilised to scan the network for connected
devices and check them against known devices of users
'''
import subprocess
import re

# Read files for which devices are registered for each person
with open('max_devices', 'r') as handle:
    maxDevices = [l[:-1] for l in handle.readlines()]
with open('alex_devices','r') as handle:
    alexDevices = [l[:-1] for l in handle.readlines()]

# Method calls the linux command 'ip add' returning the connections status and
# ip address of each network device and parses out all valid ip 
# adresses using regex
def getIpAdresses():
    # Execute the linux command 'ip add'
    ipResponse = str(subprocess.Popen(['ip add'], shell=True, stdout=subprocess.PIPE).stdout.read())
    return re.findall(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,3}',ipResponse)

# Use the network mapping tool nmap to get all the network devices connected to
# the network specified by the given ip address
#
# parameters: ip IP address of the network nmap will scan
#
# returns: list of network devices connected to the network
def nmap(ip):
    devices = []
    # execute nmap in TCP NULL scan mode to avoid firewall blocking of ports
    nmapOutput = str(subprocess.Popen([f'sudo nmap -sn {ip}'], shell=True, stdout=subprocess.PIPE).stdout.read())
    # parse the nmap output to get all the devices connected to the network
    devices = nmapOutput.split('scan report for ')[1:]
    return devices 

# Method scans the network getting the network ip first and then calling the nmap
# method to get all the connected devices
#
# parameter: verbose if true extra consol output for debugging is given,
#           default is false
#
# returns: a list of all the devices connected to the network
def scanNetwork(verbose=False):
    # Get IP
    ips = getIpAdresses()
    # verbose mode for debugging
    if verbose:
        print(f'IP Adresses: {ips}')
    # Ethernet is the second ip returned, do nmap scan
    devices = nmap(ips[1])
    return [device.split(' ')[0] for device in devices]

# Method checks for all devices in the network and then checks them against the
# known devices for each person
#
# returns: a touple of lists containing the found known devices for each user
def checkWhoIsHome(verbose = False):
    # get all network devices
    deviceNames = scanNetwork(verbose=verbose)
    # verbose mode for debugging
    if verbose:
        print(f'All found Devices: {deviceNames}')
    # get the interection of the set of all the devices belonging to 
    # alex or maexchen with the list of devices on the network as a list
    maxDevicesIntersection = list(set(maxDevices).intersection(deviceNames))
    alexDevicesIntersection = list(set(alexDevices).intersection(deviceNames))
    
    return maxDevicesIntersection, alexDevicesIntersection

# Do a verbose network scan for testing before integration in
# the webserver script
def verboseOutput():
    mD, aD = checkWhoIsHome(verbose=True)
    if len(mD) > 0:
        print(f'Maexchen ist zu Hause! Gefundene Devices: {mD}')
    if len(aD) > 0:
        print(f'Alex ist zu Hause! Gefundene Devices: {aD}')


# Run the verbose scan if not loaded as a module
if  __name__ == '__main__':
    print('Running in standalone mode')
    verboseOutput()
