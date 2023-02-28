import time
import simpleNetworkScanner as sns

threshold = 600 # threshold in seconds

maxLastOnlineTime = time.time()
alexLastOnlineTime = time.time()


def checkWhoIsHome():
    devices = sns.checkWhoIsHome()
    maxIsHome = len(devices[0]) > 0
    alexIsHome = len(devices[1]) > 0

    return maxIsHome, alexIsHome

def writeToFile(filename, value):
    with open(f'{filename}.bool', 'w') as handle:
        handle.write(str(value))

def parseOnlineTime(name, value, lastOnlineTime):
    if not value and abs(lastOnlineTime-time.time()) > threshold:
        writeToFile(name, False)
    elif value:
        writeToFile(name, True)
        lastOnlineTime = time.time()
        return lastOnlineTime


if __name__ == '__main__':

    try:
        while True:
            maxBool, alexBool = checkWhoIsHome()
            maxLastOnlineTime = parseOnlineTime('max', maxBool, maxLastOnlineTime)
            alexLastOnlineTime = parseOnlineTime('alex', alexBool, alexLastOnlineTime)
            time.sleep(30)
            
    except KeyboardInterrupt:
        pass