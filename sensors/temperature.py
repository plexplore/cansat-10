import logging
from models.sensor import Sensor, SensorType, SensorData
from board import I2C
from bmp180 import BMP180
from adafruit_mpu6050 import MPU6050
from threading import Lock


class TemperatureBMP180Sensor(Sensor):
    def __init__(self, _id: int, i2c_lock: Lock):
        self.id = _id
        self.sensor_type = SensorType.TEMPERATURE_BMP180
        self.logger = logging.getLogger("temperature-bmp180-sensor_" + str(_id))
        self.i2c = I2C()
        self.i2c_lock = i2c_lock
        self.bmp = BMP180(self.i2c)
        super().__init__(self.sensor_type)

    def get_data(self) -> SensorData:
        with self.i2c_lock:
            res = self.bmp.temperature
        return SensorData(self.id, self.sensor_type, res)


class TemperatureMPU6050Sensor(Sensor):
    def __init__(self, _id: int, i2c_lock: Lock):
        self.id = _id
        self.sensor_type = SensorType.TEMPERATURE_MPU6050
        self.logger = logging.getLogger("temperature-mpu6050-sensor_" + str(_id))
        self.i2c = I2C()
        self.i2c_lock = i2c_lock
        self.mpu = MPU6050(self.i2c)
        super().__init__(self.sensor_type)

    def get_data(self) -> SensorData:
        with self.i2c_lock:
            res = self.mpu.temperature
        return SensorData(self.id, self.sensor_type, res)
