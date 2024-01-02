from abc import ABC, abstractmethod
import time as t
from enum import Enum
import uuid


class SensorType(Enum):
    DUMMY = 1
    TEMPERATURE = 2
    PRESSURE = 3
    GYRO = 4


class SensorData:
    def __init__(self, sensor_id: int, time: t.time, data):
        self.sensor_id = sensor_id
        self.time = time
        self.data_id = str(uuid.uuid4())
        self.data = data
        self.send = False
        self.saved = False


class Sensor(ABC):
    def __init__(self, sensor_type: SensorType):
        self.sensor_type = sensor_type

    @abstractmethod
    def get_data(self) -> SensorData:
        pass


class SensorInstance:
    def __init__(self, sensor: Sensor):
        self.sensor = sensor
