"""
# Event simulated: User entering the house.
"""
import sys
sys.path.append('/Users/nehayadav/Downloads/DosLab2/spring17-lab2-ayush-sharma-umass/src')
import time
import Pyro4
import constants.Constants as constants
from sensor.Sensor import Sensor
from device.Device import Device
from gateway.Gateway import Gateway
from gateway.Database import Database
import constants.Constants as constants
import timeit

print("---------------------------------------------------------------------------------")
print("Leader Election")
proxyObj = Pyro4.Proxy(constants.ServerConstants.PYRONAME + constants.ProcessNames.GATEWAY)
print("{} told {} to  {}".format(constants.ProcessNames.MANAGER,
                                 constants.ProcessNames.GATEWAY, constants.MessageConstants.INITIATE_ELECTION))
uriList = [constants.ProcessNames.TEMPERATURE, constants.ProcessNames.BEACON, constants.ProcessNames.DOOR,
           constants.ProcessNames.MOTION, constants.ProcessNames.BULB, constants.ProcessNames.OUTLET,
           constants.ProcessNames.GATEWAY]
proxyObj.triggerElection(constants.MessageConstants.INITIATE_ELECTION, uriList,
                         constants.ProcessNames.MANAGER, proxyObj.getVectorClock())


iotProcess = uriList

TimeServer = None
for process in iotProcess:
	uri = constants.ServerConstants.PYRONAME + process
	proxyObj = Pyro4.Proxy(uri)
	if (proxyObj.getTimeServer(proxyObj.getVectorClock())):
		TimeServer = process
		print("Elected TimeServer is {}".format(process))

print("Leader Election Process Completed")
print("---------------------------------------------------------------------------------")
print("Clock syncronization")
uri = constants.ServerConstants.PYRONAME + TimeServer
proxyObj = Pyro4.Proxy(uri)
proxyObj.clock_syncronize(iotProcess,proxyObj.getVectorClock())
for process in iotProcess:
	uri = constants.ServerConstants.PYRONAME + process
	proxyObj = Pyro4.Proxy(uri)
	print("{} timestamp : {:.1f}".format(process,proxyObj.getTimeStamp(proxyObj.getVectorClock())))
print("Clock syncronization done")

print("---------------------------------------------------------------------------------")
for process in iotProcess:
	uri = constants.ServerConstants.PYRONAME + process
	proxyObj = Pyro4.Proxy(uri)
	print("Process ({}) , vectorClock: {}".format(process,proxyObj.getVectorClock()))


time.sleep(5)


# User turns on the beacon
uri = constants.ServerConstants.PYRONAME + constants.ProcessNames.BEACON
beacon = Pyro4.Proxy(uri)
#beacon.changeState(constants.SensorConstants.STATE_ON)
vclock = beacon.getVectorClock()
print vclock
beacon.changeState("ON")


# OPEN THE DOOR
# Change the current state of DOOR to OPEN
uri = constants.ServerConstants.PYRONAME + constants.ProcessNames.DOOR
door = Pyro4.Proxy(uri)
door.changeState(constants.SensorConstants.STATE_ON)

# HOLD THE DOOR
# HOLD THE DOOR
# HOLD THE DOOR
# HOLD THE DOOR
# HODOR
# HODOR
# HODOR


# Close the Door.
# Change the current state of DOOR to CLOSE
door.changeState(constants.SensorConstants.STATE_OFF)


# Motion sensor senses motion and passes to Gateway
uri = constants.ServerConstants.PYRONAME + constants.ProcessNames.MOTION
motion = Pyro4.Proxy(uri)
motion.changeState(constants.SensorConstants.STATE_ON)


# ask database to generate inference from the events
uri = constants.ServerConstants.PYRONAME + constants.ProcessNames.GATEWAY
gateway = Pyro4.Proxy(uri)
gateway.getInference()

uri = constants.ServerConstants.PYRONAME + constants.ProcessNames.GATEWAY
gateway = Pyro4.Proxy(uri)
startTime = timeit.default_timer()
gateway.getVectorClock()
endTime = timeit.default_timer()
difference = (endTime - startTime)/2
print("User quried gateway for information and gateway returned information")
print("Network Latency {}".format(difference))

# Computing the latency

uri = constants.ServerConstants.PYRONAME + constants.ProcessNames.DATABASE
databse = Pyro4.Proxy(uri)
startTime = timeit.default_timer()
databse.getID()
endTime = timeit.default_timer()
difference = (endTime - startTime)/2
print("User quried gateway for information and gateway queried information from database and returned")
print("Total Network Latency {}".format(difference))
uri = constants.ServerConstants.PYRONAME + constants.ProcessNames.DATABASE
databse = Pyro4.Proxy(uri)
startTime = timeit.default_timer()
databse.getID()
endTime = timeit.default_timer()
difference = endTime - startTime
print("User quried gateway for information and gateway queried information from database and returned")
print("Total Network Latency {}".format(difference))
