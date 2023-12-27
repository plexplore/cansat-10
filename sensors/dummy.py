import random
import time

from models.sensor import Sensor, SensorType, SensorData


class DummySensor(Sensor):
    def __init__(self):
        super().__init__(1, "DummySensor", SensorType.DUMMY)

    def get_data(self) -> SensorData:
        time.sleep(0.01)
        return SensorData(self.sensor_id, self.sensor_type, random.randint(0, 1000))
