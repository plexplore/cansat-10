import logging
from models.sensor import Sensor, SensorType, SensorData
from board import I2C
from bmp180 import BMP180
from threading import Lock


class AltitudeSensor(Sensor):
    def __init__(self, _id: int, i2c_lock: Lock):
        self.id = _id
        self.sensor_type = SensorType.ALTITUDE
        self.logger = logging.getLogger("altitude-sensor_" + str(_id))
        self.i2c = I2C()
        self.i2c_lock = i2c_lock
        self.bmp = BMP180(self.i2c)
        super().__init__(self.sensor_type)

    def get_data(self) -> SensorData:
        with self.i2c_lock:
            res = self.bmp.altitude
        return SensorData(self.id, self.sensor_type, res)

