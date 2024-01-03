from threading import Thread, Lock, Event
from models.sensor import Sensor, SensorData
import time

class SensorService(Thread):
    def __init__(self, sensor: Sensor, data: list[SensorData], data_lock: Lock, ex_e: Event, rq_per_sec=10):
        super(SensorService, self).__init__()
        self.sensor = sensor
        self.data = data
        self.data_lock = data_lock
        self.rq_per_sec = rq_per_sec
        self.ex_e = ex_e

    def run(self):
        t = 0.0
        while not self.ex_e.wait(timeout=t):
            ts = time.time()
            sd = self.sensor.get_data()
            with self.data_lock:
                self.data.append(sd)
            t = min(0.0, (1/self.rq_per_sec)-(time.time()-ts))
