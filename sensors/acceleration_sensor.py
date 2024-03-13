import json
import logging
import time
import serial

from models.sensor import Sensor, SensorType, SensorData

from threading import Lock
from board import I2C
from adafruit_mpu6050 import MPU6050


class AccelerationSensor(Sensor):
    def __init__(self, _id: int, i2c_lock: Lock):
        self.id = _id
        self.sensor_type = SensorType.ACCELERATION
        self.logger = logging.getLogger("acceleration-sensor_" + str(_id))
        self.i2c = I2C()
        self.i2c_lock = i2c_lock
        self.mpu = MPU6050(self.i2c)
        super().__init__(self.sensor_type)

    def get_data(self) -> SensorData:
        with self.i2c_lock:
            res = [self.mpu.acceleration]
        return SensorData(self.id, self.sensor_type, res)

class DebugAccelerationSensor(Sensor):
    def __init__(self, _id: int, port: str, baudrate: int):
        self.id = _id
        self.sensor_type = SensorType.ACCELERATION
        self.port = port
        self.baudrate = baudrate
        self.logger = logging.getLogger("debug-acceleration-sensor_" + str(_id))
        super().__init__(self.sensor_type)

    def get_data(self) -> SensorData:
        time.sleep(0.02)
        with serial.Serial(self.port, self.baudrate, timeout=1, stopbits=2) as ser:
            res = {}
            while True:
                try:
                    data = ser.readline().decode("utf-8")
                    res = json.loads(json.loads(data)["beschl"])
                except Exception as e:
                    self.logger.warning(f"Could not decode on sensor {self.id} - retrying")
                    continue
                break
        return SensorData(self.id, self.sensor_type, res)


if __name__ == '__main__':
    s = DebugAccelerationSensor(1, "COM5", 115200)
    print(s.get_data())