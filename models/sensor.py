from abc import ABC, abstractmethod
import datetime as dt
from enum import Enum
import uuid
from db.db_models import BaseSensorData, CanSatSession


class SensorType(Enum):
    DUMMY = 1
    TEMPERATURE_BMP180 = 2
    PRESSURE = 3
    GYRO = 4
    ACCELERATION = 5
    ALTITUDE = 6
    TEMPERATURE_MPU6050 = 7


class SensorData:
    def __init__(self, sensor_id: int, sensor_type: SensorType, data):
        self.sensor_id = sensor_id
        self.time: dt.datetime = dt.datetime.now()
        self.sensor_type = sensor_type
        self.data_id = str(uuid.uuid4())
        self.data: list[float] = data
        self.send = False
        self.saved = False

    def to_base_sensor_data(self, session: CanSatSession) -> BaseSensorData:
        d = self.data
        while len(d) < 3:
            d.append(0.0)
        d1, d2, d3 = d

        return BaseSensorData(time=self.time, sensor_id=self.sensor_id, sensor_type=str(self.sensor_type),
                              data_id=self.data_id, d1=d1, d2=d2, d3=d3, session=session)

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
    elif sensor_type.lower() == "temperature_bmp180":
        return SensorType.TEMPERATURE_BMP180
    elif sensor_type.lower() == "presssure":
        return SensorType.PRESSURE
    elif sensor_type.lower() == "altitude":
        return SensorType.ALTITUDE
    elif sensor_type.lower() == "temperature_mpu6050":
        return SensorType.TEMPERATURE_MPU6050

    return SensorType.DUMMY


def get_sensor_dimensions(sensor_type: SensorType) -> int:
    if sensor_type in [SensorType.GYRO, SensorType.ACCELERATION]:
        return 3
    return 1
