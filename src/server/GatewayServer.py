import Pyro4
import sys
import os
#print os.getcwd() 
sys.path.append('/Users/nehayadav/Downloads/DosLab2/spring17-lab2-ayush-sharma-umass/src')
import constants.Constants as constants
from gateway.Gateway import Gateway


daemon = Pyro4.Daemon()

# finds the name server
nameServer = Pyro4.locateNS()

Gateway(constants.ProcessNames.GATEWAY, daemon, nameServer,constants.VectorClock.VECTORCLOCK)

print("Gateway registered.")

daemon.requestLoop()


