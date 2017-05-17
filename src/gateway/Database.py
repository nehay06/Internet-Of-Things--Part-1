import Pyro4
import sys
sys.path.append('/Users/nehayadav/Downloads/DosLab2/spring17-lab2-ayush-sharma-umass/src')
import constants.Constants as constants
import random
import os

@Pyro4.expose
class Database:

    def __init__(self, name, gateWayName, daemon, nameserver):
        """
        The constructor to set up a Database.

        :param name: the name to identify on NameServer
        :param gateWayName: the logical name of Gateway
        :param daemon: the daemon process
        :param nameserver: the nameserver
        """
        self._type = constants.ProcessConstants.TYPE_DATABASE
        self._name = name
        self._gatewayName = gateWayName
        self._ID = None
        self.eligible = True
        self.fileName = "databaseRecord.txt"

        try:
            filePath = "./" + self.fileName
            os.remove(filePath)
        except OSError:
            pass

        self._registerOnServer(daemon, nameserver)
        self.registerWithGateway()



    def _registerOnServer(self, daemon, nameserver):
        """
        Registering on Pyro Server.
        :param daemon: daemon process
        :param nameserver: nameserver
        :return: None
        """
        uri = daemon.register(self)
        nameserver.register(self._name,uri)
        print("Device registered. Name {} ".format(self._name))


    def registerWithGateway(self):
        uri = "PYRONAME:"+self._gatewayName
        gatewayProxy = Pyro4.Proxy(uri)
        print("Registering {} with gateWay: {} and gatewayProxy: {}".format(self._name,self._gatewayName,gatewayProxy))
        self._ID = gatewayProxy.register(self._type, self._name,None)


    def queryHistory(self):
        """[summary]
        
        [returns the recent events from the database]
         
        Returns:
            [list] -- [returns a list containing all the recent events]
        """
        filePath = "./" + self.fileName
        output = []
        counter = 1
        for line in open(filePath).readlines():
            stringData = line.rstrip().split(" ")
            if counter <= constants.DatabaseConstants.MAX_RECENT_FILES:
                output.append(stringData)
                counter += 1
            else:
                break
        return output

    def recordState(self, deviceID, state,ptype,name,timeStamp,vectorClock):
        """
        writes in to DB
        :param deviceID: INTEGER
        :param state: STATE
        :return: none
        """
        print("Storing state for {}".format(name))
        filePath = "./" + self.fileName

        if not os.path.isfile(filePath):
            file = open(filePath, "w")
        else:
            file = open(filePath, "a")

        print("Storing state for {}".format(name))
        stringData = str(deviceID) + " " + name + " " + str(ptype) + " " + state + " "+ str(timeStamp)+ " " + str(vectorClock)+"\n"
        print("String data {}".format(stringData))
        file.write(stringData)
        file.close()


    def readState(self, deviceID):
        """
        return the state of the device ID
        :param deviceID: INTEGER
        :return: state
        """
        filePath = "./" + self.fileName
        state = None
        for line in reversed(open(filePath).readlines()):
            stringData = line.rstrip().split(" ")
            if stringData[0] == deviceID:
                state = stringData
                break

        return state

    def getEligibleStatus(self):
        return self.eligible

    def getID(self):
        return self._ID

