# This module contains all the constants.


class ProcessConstants:
    TYPE_GATEWAY = 1
    TYPE_SENSOR = 2
    TYPE_SENSOR_TEMPERATURE = 3
    TYPE_SENSOR_MOTION = 4
    TYPE_SENSOR_DOOR = 5
    TYPE_DEVICE = 6
    TYPE_DATABASE = 7

class ProcessNames:
    TEMPERATURE = "Temperature"
    DOOR = "Door"
    MOTION = "Motion"
    BULB = "Bulb"
    OUTLET ="Outlet"
    GATEWAY ="GateWay"
    DATABASE = "Database"
    BEACON = "Beacon"
    MANAGER = "Manager"

class SensorConstants:
    MAX_SENSORS = 3
    STATE_OFF = "OFF"
    STATE_ON = "ON"
    DEFAULT_TEMP = 30

class GatewayConstants:
    MAX_GATEWAY = 1


class DeviceConstants:
    MAX_DEVICE = 2
    STATE_OFF = "OFF"
    STATE_ON = "ON"

class DatabaseConstants:
    MAX_RECENT_FILES = 5

class MessageConstants:
    INITIATE_ELECTION = "INITIATE_ELECTION"
    ELECTION = "ELECTION"
    OK  = "OK"

class ServerConstants:
    PYRONAME = "PYRONAME:"
    SERVER_HOST = "localhost"
    SERVER_PORT = 9090




class VectorClock:
    VECTORCLOCK = {"Temperature":0,"Door":0,"Motion":0,"Bulb":0,"Outlet":0,"GateWay":0,"Beacon":0}

class DataBase:
    DATABASE_SCHEMA_INDEX = {0: "deviceID", 1: "state", 2: "ptype",3: "name",4:"timeStamp",5:"vectorClock"}


class Events:
    EXIT = [ProcessNames.MOTION,ProcessNames.DOOR,ProcessNames.DOOR]
    ENTRY = [ProcessNames.BEACON,ProcessNames.DOOR,ProcessNames.DOOR,ProcessNames.MOTION]
    BURGLAR = [ProcessNames.DOOR,ProcessNames.DOOR,ProcessNames.MOTION]
