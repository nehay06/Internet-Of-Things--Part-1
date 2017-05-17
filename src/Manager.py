import Pyro4
import constants.Constants as constants
from sensor.Sensor import Sensor
from device.Device import Device
from gateway.Gateway import Gateway
from gateway.Database import Database
import constants.Constants as constants

print("---------------------------------------------------------------------------------")
print("Leader Election")
proxyObj = Pyro4.Proxy("PYRONAME:GateWay")
print("{} told {} to  {}".format("Manager","Gateway","initiateElection"))
proxyObj.triggerElection("initiateElection",["Temperature","Door","Motion","Bulb","Outlet","GateWay"],"Manager",proxyObj.getVectorClock())


iotProcess = ["Temperature","Door","Motion","Bulb","Outlet","GateWay"]

TimeServer = None
for process in iotProcess:
	uri = "PYRONAME:"+process
	proxyObj = Pyro4.Proxy(uri)
	if (proxyObj.getTimeServer(proxyObj.getVectorClock())):
		TimeServer = process
		print("Elected TimeServer is {}".format(process))
print("Leader Election Process Completed")
print("---------------------------------------------------------------------------------")
print("Clock syncronization")
uri = "PYRONAME:"+TimeServer
proxyObj = Pyro4.Proxy(uri)
proxyObj.clock_syncronize(iotProcess,proxyObj.getVectorClock())
for process in iotProcess:
	uri = "PYRONAME:"+process
	proxyObj = Pyro4.Proxy(uri)
	print("{} timestamp : {:.1f}".format(process,proxyObj.getTimeStamp(proxyObj.getVectorClock())))
print("Clock syncronization done")

print("---------------------------------------------------------------------------------")
for process in iotProcess:
	uri = "PYRONAME:"+process
	proxyObj = Pyro4.Proxy(uri)
	print("Process ({}) , vectorClock: {}".format(process,proxyObj.getVectorClock()))