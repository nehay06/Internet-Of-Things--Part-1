import Pyro4
import sys
sys.path.append('/Users/nehayadav/Downloads/DosLab2/spring17-lab2-ayush-sharma-umass/src')
import constants.Constants as constants
from device.Device import Device

daemon = Pyro4.Daemon()

# finds the name server
nameServer = Pyro4.locateNS()

Device(constants.ProcessNames.BULB, constants.ProcessNames.GATEWAY, constants.DeviceConstants.STATE_OFF,
       daemon,nameServer,constants.VectorClock.VECTORCLOCK)


print("Device Bulb registered.")

daemon.requestLoop()