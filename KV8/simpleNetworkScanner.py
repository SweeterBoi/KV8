import subprocess
import re

with open('max_devices', 'r') as handle:
    maxDevices = [l[:-1] for l in handle.readlines()]
with open('alex_devices','r') as handle:
    alexDevices = [l[:-1] for l in handle.readlines()]

def getIpAdresses():

    ipResponse = str(subprocess.Popen(['ip add'], shell=True, stdout=subprocess.PIPE).stdout.read())
    
    ips = re.findall(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,3}',ipResponse)
    return ips

def nmap(ip):
    devices = []

    nmapOutput = str(subprocess.Popen([f'sudo nmap -sn {ip}'], shell=True, stdout=subprocess.PIPE).stdout.read())
    devices = nmapOutput.split('scan report for ')[1:]
    return devices 

def scanNetwork(verbose=False):
    ips = getIpAdresses()
    if verbose:
        print(f'IP Adresses: {ips}')
    devices = nmap(ips[1])
    deviceNames = []
    for device in devices:
        deviceNames.append(device.split(' ')[0])
    return deviceNames
    
def checkWhoIsHome(verbose = False):
    deviceNames = scanNetwork(verbose=verbose)
    if verbose:
        print(f'All found Devices: {deviceNames}')
    maxDevicesIntersection = list(set(maxDevices).intersection(deviceNames))
    alexDevicesIntersection = list(set(alexDevices).intersection(deviceNames))
    
    return maxDevicesIntersection, alexDevicesIntersection

def verboseOutput():
    mD, aD = checkWhoIsHome(verbose=True)
    if len(mD) > 0:
        print(f'Maexchen ist zu Hause! Gefundene Devices: {mD}')
    if len(aD) > 0:
        print(f'Alex ist zu Hause! Gefundene Devices: {aD}')



if  __name__ == '__main__':
    print('Running in standalone mode')
    verboseOutput()
