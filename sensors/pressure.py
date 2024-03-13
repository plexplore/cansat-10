import logging
from models.sensor import Sensor, SensorType, SensorData
from board import I2C
from bmp280 import BMP280
from threading import Lock


class PressureSensor(Sensor):
    def __init__(self, _id: int, i2c_lock: Lock):
        self.id = _id
        self.sensor_type = SensorType.PRESSURE
        self.logger = logging.getLogger("pressure-sensor_" + str(_id))
        self.i2c: I2C = I2C()
        self.i2c_lock = i2c_lock
        self.bmp = BMP280(i2c_addr=0x76)
        super().__init__(self.sensor_type)

    def get_data(self) -> SensorData:
        with self.i2c_lock:
            res = [self.bmp.get_pressure()]
        return SensorData(self.id, self.sensor_type, res)

