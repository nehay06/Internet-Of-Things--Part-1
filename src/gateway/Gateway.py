import Pyro4
import sys
sys.path.append('/Users/nehayadav/Downloads/DosLab2/spring17-lab2-ayush-sharma-umass/src')
import constants.Constants as constants
import random
from time import time
import timeit

@Pyro4.expose
class Gateway:

    def __init__(self, name, daemon, nameserver,vectorClock):
        """
        Constructor to set up the Gateway.

        :param name: the name to identify on NameServer
        :param daemon: the daemon process
        :param nameserver: the nameserver
        """
        self._type = constants.ProcessConstants.TYPE_GATEWAY
        self._name = name
        self._ID = 1

        self._IDtoTypeMap = {}
        self._databaseName = None
        self._counter = 1
        self.eligible = True
        self.timeServer = False
        self.timeStamp = time()
        self.vectorClock = vectorClock

        self._registerOnServer(daemon, nameserver,self.vectorClock)



    def _registerOnServer(self, daemon, nameserver,vclock):
        """
        Registering on Pyro Server.
        :param daemon: the daemon process.
        :param nameserver: the nameServer.
        :return: None
        """
        uri = daemon.register(self)
        nameserver.register(self._name, uri)
        self.updateVectorClock(vclock)
        print("Gateway registered. Name {} and uri {} ".format(self._name,uri))


    def getVectorClock(self):
        return self.vectorClock

    def register(self, type, name,vclock):
        """
        Other devices/sensors call this function to regiter themselves with Gateway
        :param type: the type of process that makes this call
        :param name: the name with which it wants to register. This name is the proxyName.
        :return: INTEGER: a global ID.
        """
        print ("Gateway Registry invoked for {}".format(name))
        if vclock is not None:
            self.updateVectorClock(vclock)
        self._IDtoTypeMap[self._counter] = (name, type)
        if type == constants.ProcessConstants.TYPE_DATABASE:
            self._databaseName = name
        self._counter += 1
        return self._counter

    
    def getEligibleStatus(self,vclock):
        self.updateVectorClock(vclock)

        return self.eligible

    def electionResult(self,message,vclock):
        self.updateVectorClock(vclock)
        print("I'm {} and {}".format(self._name,message))

    def informElectionResult(self,message,UriArray,vclock):
        self.updateVectorClock(vclock)
        for process in UriArray:
            if process !=self._name:
                uri = "PYRONAME:"+process
                proxyObj = Pyro4.Proxy(uri)
                proxyObj.electionResult(message,self.vectorClock)

    def getTimeStamp(self,vclock):
        self.updateVectorClock(vclock)
        return self.timeStamp

    def updateTimeStamp(self,offset,vclock):
        self.updateVectorClock(vclock)
        self.timeStamp +=  offset
        print("My ({}) Updated TimeStamp is {}".format(self._name,self.timeStamp))

    def clock_syncronize(self,UriArray,vclock):
        self.updateVectorClock(vclock)
        timestamp = dict()
        totalTimeStamp = 0
        for process in UriArray:
            if self._name != process:
                uri = "PYRONAME:"+process
                proxyObj = Pyro4.Proxy(uri)
                timestamp[process] = proxyObj.getTimeStamp(self.vectorClock)
                totalTimeStamp +=  timestamp[process]
            else:
                timestamp[process] = self.getTimeStamp(self.vectorClock)
                totalTimeStamp +=  timestamp[process]
        average = totalTimeStamp/len(timestamp)

        for process in UriArray:
            uri = "PYRONAME:"+process
            proxyObj = Pyro4.Proxy(uri)
            print("Process {} TimeStamp before clock sync {} ".format(process,timestamp[process]))
            proxyObj.updateTimeStamp(average-timestamp[process],self.vectorClock)
            print("Process {} TimeStamp after clock sync {:.1f} ".format(process,average))
    
    def getTimeServer(self,vclock):
        self.updateVectorClock(vclock)
        return self.timeServer

    def updateVectorClock(self,vclock):
        for key,value in vclock.items():
            if key == self._name:
                self.vectorClock[key] = max(self.vectorClock[key],value)+1
            else:
                self.vectorClock[key] = max(self.vectorClock[key],value)

    def triggerElection(self,message,UriArray,callerName,vclock):
        self.updateVectorClock(vclock)
        if message == constants.MessageConstants.OK:
            self.eligible = False
            print("{} told {}".format(callerName,message))
        
        if self.eligible == False:
            pass
        else:
            if message == constants.MessageConstants.ELECTION or message == constants.MessageConstants.INITIATE_ELECTION:
                print("{} requested {}".format(callerName,message))
                rand =  '{:.2f}'.format(random.random())
                if rand >= .95:
                    if callerName != constants.ProcessNames.MANAGER:
                        uri = "PYRONAME:"+callerName
                        proxyObj = Pyro4.Proxy(uri)
                        proxyObj.triggerElection(constants.MessageConstants.OK,UriArray,self._name,self.vectorClock)
                        print("I ({}) told OK to {}".format(self._name,callerName))
                    for process in UriArray:
                        if process != callerName and process != self._name:
                            uri = "PYRONAME:"+process
                            proxyObj = Pyro4.Proxy(uri)
                            if proxyObj.getEligibleStatus(self.vectorClock) == True:
                                print("I ({}) requested election to {}".format(self._name,process))
                                proxyObj.triggerElection(constants.MessageConstants.ELECTION,UriArray,self._name,self.vectorClock)
                    if self.eligible == True:
                        self.timeServer = True
                        # message = self._name +" is the leader"
                        # self.informElectionResult(message,UriArray) 
                else:
                    self.eligible = False

    def reportState(self, deviceID, state, ptype,name,timestamp,vectorClock):
        """

        :param deviceID: The ID of the caller.
        :param state: The current state of the caller.
        :param vclock: The vClock of the caller.
        :return:
        """
        self.updateVectorClock(vectorClock)
        print("Inside Gateway Reporting {} state".format(name))
        databaseProxy = Pyro4.Proxy(constants.ServerConstants.PYRONAME + self._databaseName)
        databaseProxy.recordState(deviceID, state,ptype,name,timestamp,vectorClock[name])


    def checkLatency(self):
        uri = constants.ServerConstants.PYRONAME + constants.ProcessNames.DATABASE
        databse = Pyro4.Proxy(uri)
        return databse.getID()

    def getInference(self):
        uri = "PYRONAME:Database"
        database = Pyro4.Proxy(uri)
        eventsHistory = database.queryHistory()
        eventOrdering = []
        #DATABASE_SCHEMA_INDEX = {0: deviceID, 1: state, 2: ptype,3: name,4:timeStamp,5:vectorClock}
        #uriList = [constants.ProcessNames.TEMPERATURE, constants.ProcessNames.BEACON, constants.ProcessNames.DOOR,
           #constants.ProcessNames.MOTION, constants.ProcessNames.BULB, constants.ProcessNames.OUTLET,
           #constants.ProcessNames.GATEWAY]
        for event in eventsHistory:
            if event[1] == constants.ProcessNames.DOOR or event[1] == constants.ProcessNames.MOTION or event[1] == constants.ProcessNames.BEACON :
                eventOrdering.append(event[1])
        if constants.Events.ENTRY == eventOrdering:
            print("User Entered the house")
            print("Turning on lights")
            print("Security state set to OFF")
            print("System state set to Home")
        if constants.Events.EXIT == eventOrdering:
            print("User Left the house")
            print("Turning OFF lights")
            print("Security state set to ON")
            print("System state set to AWAY")

        if constants.Events.BURGLAR == eventOrdering:
            print("Alaram: Burglar entered the house")
            print("Turning on lights")
            print("Security state set to ALARM")
            print("System state set to AWAY")



