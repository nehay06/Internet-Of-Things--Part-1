import Pyro4
import sys
sys.path.append('/Users/nehayadav/Downloads/DosLab2/spring17-lab2-ayush-sharma-umass/src')
import constants.Constants as constants
from gateway.Database import Database


daemon = Pyro4.Daemon()

# finds the name server
nameServer = Pyro4.locateNS()

Database(constants.ProcessNames.DATABASE,constants.ProcessNames.GATEWAY, daemon, nameServer)

print("Database registered.")

daemon.requestLoop()