from abc import ABC, abstractmethod
import time as t
from enum import Enum


class SensorType(Enum):
    DUMMY = 1
    TEMPERATURE = 2
    PRESSURE = 3


class SensorData:
    def __init__(self, sensor_id: int, time: t.time, data):
        self.sensor_id = sensor_id
        self.time = time
        self.data = data


class Sensor(ABC):
    def __init__(self, sensor_id: int, sensor_name: str, sensor_type: SensorType):
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type

    @abstractmethod
    def get_data(self) -> SensorData:
        pass
