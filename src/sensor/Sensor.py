import Pyro4
import sys
sys.path.append('/Users/nehayadav/Downloads/DosLab2/spring17-lab2-ayush-sharma-umass/src')
import constants.Constants as constants
import random
from time import time

@Pyro4.expose
class Sensor:


    def __init__(self, name, gateWayName, state, daemon, nameserver,vectorClock):
        """
        The constructor to set up a Sensor.

        :param name: the name to identify on NameServer
        :param gateWayName: the logical name of Gateway
        :param state: the initial state of the Sensor
        :param daemon: the daemon process
        :param nameserver: the nameserver
        """
        self._type = constants.ProcessConstants.TYPE_SENSOR
        self._name = name
        self._gatewayName = gateWayName
        self._state = state
        self._ID = None
        self.eligible = True
        self.timeServer = False
        self.timeStamp = time()
        self.vectorClock = vectorClock

        self._registerOnServer(daemon, nameserver,self.vectorClock)
        self.registerWithGateway(self.vectorClock)


    def _registerOnServer(self, daemon, nameserver,vclock):
        """
        Registering on Pyro Server.
        :param daemon: daemon process
        :param nameserver: nameserver
        :return: None
        """
        uri = daemon.register(self)
        nameserver.register(self._name, uri)
        self.updateVectorClock(vclock)
        print("Device registered. Name {} ".format(self._name))


    def getVectorClock(self):
        return self.vectorClock

    def registerWithGateway(self,vclock):
        self.updateVectorClock(vclock)
        uri = "PYRONAME:"+self._gatewayName
        gatewayProxy = Pyro4.Proxy(uri)
        self._ID = gatewayProxy.register(self._type, self._name,self.vectorClock)

    def get_state(self,vclock):
        self.updateVectorClock(vclock)
        return self._state


    def getGlobalId(self,vclock):
        self.updateVectorClock(vclock)
        return self._ID

    def getEligibleStatus(self,vclock):
        self.updateVectorClock(vclock)
        return self.eligible
 
    def informElectionResult(self,message,UriArray,vclock):
        self.updateVectorClock(vclock)
        for process in UriArray:
            if process !=self._name:
                uri = "PYRONAME:"+process
                proxyObj = Pyro4.Proxy(uri)
                proxyObj.electionResult(message)
    
    def getTimeStamp(self,vclock):
        self.updateVectorClock(vclock)
        return self.timeStamp

    def updateTimeStamp(self,offset,vclock):
        self.updateVectorClock(vclock)
        self.timeStamp += offset
        print("My ({}) Updated TimeStamp is {}".format(self._name,self.timeStamp))

    def getTimeServer(self,vclock):
        self.updateVectorClock(vclock)
        return self.timeServer

    def updateVectorClock(self, vclock):
        for key,value in vclock.items():
            if key == self._name:
                self.vectorClock[key] = max(self.vectorClock[key],value)+1
            else:
                self.vectorClock[key] = max(self.vectorClock[key],value)

    def electionReslut(self,message,vclock):
        self.updateVectorClock(vclock)
        print("I'm {} and {}".format(self._name,message))

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
            proxyObj.updateTimeStamp(average-timestamp[process])
            print("Process {} TimeStamp after clock sync {:.1f} ".format(process,average))

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
    
    def changeState(self, state):
        print "Going to change state to Sensor"
        self._state = state

        # do self clock operations
        self.updateVectorClock(self.vectorClock)

        # call gateway to report state change - push message
        # This updates self vector clock and updats in the Gateway.
        self.pushState()

    def pushState(self):
        """
        Door is push-based primarily. But can also be pulled from.
        Motion is push based.
        Temperature is pull based.
        :param vclock:
        :return:
        """
        uri = "PYRONAME:"+self._gatewayName
        gatewayProxy = Pyro4.Proxy(uri)
        gatewayProxy.reportState(self._ID,self._state,self._type,self._name,self.timeStamp,self.vectorClock)
               
    def query_state(self,vclock):
        self.updateVectorClock(vclock)
        return self._ID,self._state







