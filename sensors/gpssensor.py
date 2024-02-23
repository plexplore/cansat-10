import time

from gpsdclient import GPSDClient

from models.sensor import Sensor, SensorType, SensorData
from threading import Lock, Thread
import logging
class GPSSensor(Sensor):
    def __init__(self, _id:int, serial_lock: Lock):
        self.id = _id
        self.serial_lock = serial_lock
        self.sensor_type = SensorType.GPS
        self.logger = logging.getLogger("gps-sensor_" + str(_id))
        self.session = GPSThread()
        self.session.start()
        super().__init__(self.sensor_type)

    def get_data(self) -> SensorData:
        with self.serial_lock:
            res = []
        return SensorData(self.id, self.sensor_type, res)

class GPSThread(Thread):
    def __init__(self):
        super(GPSThread, self).__init__()
        self.last_data = {}
        self.daemon = True

    def run(self) -> None:
        while True:
            with GPSDClient() as client:
                for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
                    self.last_data = result

if __name__ == '__main__':
    pass
