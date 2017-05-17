import Pyro4
import sys
sys.path.append('/Users/nehayadav/Downloads/DosLab2/spring17-lab2-ayush-sharma-umass/src')
import constants.Constants as constants
from sensor.Sensor import Sensor

daemon = Pyro4.Daemon()

# finds the name server
nameServer = Pyro4.locateNS()


#register all processes on Nameserver
Sensor(constants.ProcessNames.BEACON, constants.ProcessNames.GATEWAY, constants.SensorConstants.STATE_OFF,
       daemon,nameServer,constants.VectorClock.VECTORCLOCK)

print("Beacon sensor registered.")

daemon.requestLoop()
