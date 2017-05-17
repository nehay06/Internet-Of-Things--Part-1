import Pyro4
import constants.Constants as constants
from sensor.Sensor import Sensor
from device.Device import Device
from gateway.Gateway import Gateway
from gateway.Database import Database

daemon = Pyro4.Daemon()

# finds the name server
nameServer = Pyro4.locateNS()


#register all processes on Nameserver

Sensor("Temperature","GateWay","off",daemon,nameServer)
Sensor("Door","GateWay","off",daemon,nameServer)
Sensor("Motion","GateWay","off",daemon,nameServer)
Device("Bulb","GateWay","off",daemon,nameServer)
Device("Outlet","GateWay","off",daemon,nameServer)
Database("DataBase","GateWay",daemon,nameServer)
Gateway("GateWay",daemon,nameServer)


print("Internet of things registered")

daemon.requestLoop()
