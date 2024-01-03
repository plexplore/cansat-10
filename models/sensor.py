from abc import ABC, abstractmethod
import datetime as dt
from enum import Enum
import uuid


class SensorType(Enum):
    DUMMY = 1
    TEMPERATURE = 2
    PRESSURE = 3
    GYRO = 4
    ACCELERATION = 5


class SensorData:
    def __init__(self, sensor_id: int, sensor_type: SensorType, data):
        self.sensor_id = sensor_id
        self.time: dt.datetime = dt.datetime.now()
        self.sensor_type = sensor_type
        self.data_id = str(uuid.uuid4())
        self.data = data
        self.send = False
        self.saved = False

    def __str__(self):
        return f"{self.data_id} - {self.sensor_id} - {self.sensor_type} - {self.time.isoformat()}: {self.data}"


class Sensor(ABC):
    def __init__(self, sensor_type: SensorType):
        self.sensor_type = sensor_type

    @abstractmethod
    def get_data(self) -> SensorData:
        pass


class SensorInstance:
    def __init__(self, sensor: Sensor):
        self.sensor = sensor


def get_sensor_type(sensor_type: str) -> SensorType:
    if sensor_type.lower() == "gyro":
        return SensorType.GYRO
    elif sensor_type.lower() == "acceleration":
        return SensorType.ACCELERATION
    elif sensor_type.lower() == "temperature":
        return SensorType.TEMPERATURE

    return SensorType.DUMMY
