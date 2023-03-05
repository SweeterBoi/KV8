'''
This script defines a continuously running service that checks the network for the
connection status of user devices and asserts wether the usrs are at home currently or not
the output is writeen to .bool files
'''
import time
import simpleNetworkScanner as sns

# Threshold for how long a user must not be connected to the network
# for them to be considered offline
threshold = 100 # threshold in seconds

# initialise with 0 so the users are seen as last online on jan 1st 1970,
# which is more than the threshold would allow and thus evaluating a not
# logged in user as offline
maxLastOnlineTime = 0.0
alexLastOnlineTime = 0.0

# Method calles the simpleNetworkScanner script and check who is home
#
# returns: a tuple of booleans
def checkWhoIsHome():
    devices = sns.checkWhoIsHome()
    # users are home when at least on of their recognized dvices is logged in
    maxIsHome = len(devices[0]) > 0
    alexIsHome = len(devices[1]) > 0

    return maxIsHome, alexIsHome

# Method to write wether the user is considered online to a file
def writeToFile(filename, value):
    with open(f'{filename}.bool', 'w') as handle:
        handle.write(str(value))

# Check wether the user is offline and has not been seen for longer than the
# threshold allowes
#
# parameter: name of the user and thus file to write to; no file extension!
# parameter: value boolean indicating whether the user is considered online
# parameter: lastOnlineTime time the user was last online
#
# returns: the time the user was last online to keep a rolling memory
def parseOnlineTime(name, value, lastOnlineTime):
    if not value and abs(lastOnlineTime-time.time()) > threshold:
        writeToFile(name, False)
    elif value:
        writeToFile(name, True)
        lastOnlineTime = time.time()
    return lastOnlineTime

# Execute this if the script is run directly
if __name__ == '__main__':
    # Run until interrupted by Ctrl+C
    try:
        while True:
            # Get the state of who is home using the checkWhoIsHome method
            maxBool, alexBool = checkWhoIsHome()
            # Parse the last online time (this is written to the file from within the method)
            maxLastOnlineTime = parseOnlineTime('max', maxBool, maxLastOnlineTime)
            alexLastOnlineTime = parseOnlineTime('alex', alexBool, alexLastOnlineTime)
            time.sleep(10)
            
    except KeyboardInterrupt:
        pass