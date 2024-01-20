import gps
import time
from models.sensor import Sensor, SensorType, SensorData
from threading import Lock
import logging
class GPSSensor(Sensor):
    def __init__(self, _id:int, serial_lock: Lock):
        self.id = _id
        self.serial_lock = serial_lock
        self.sensor_type = SensorType.GPS
        self.logger = logging.getLogger("gps-sensor_" + str(_id))
        self.session = gps.gps(mode=gps.WATCH_ENABLE)
        super().__init__(self.sensor_type)

    def get_data(self) -> SensorData:
        with self.serial_lock:
            res = []
        return SensorData(self.id, self.sensor_type, res)
if __name__ == '__main__':
    session = gps.gps(mode=gps.WATCH_ENABLE)