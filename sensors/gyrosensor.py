import json
import logging
from models.sensor import Sensor, SensorType, SensorData
import serial
from threading import Lock
from board import I2C
from adafruit_mpu6050 import MPU6050


class GyroSensor(Sensor):
    def __init__(self, _id: int, i2c_lock: Lock):
        self.id = _id
        self.sensor_type = SensorType.GYRO
        self.logger = logging.getLogger("gyro-sensor_" + str(_id))
        self.i2c = I2C()
        self.i2c_lock = i2c_lock
        self.mpu = MPU6050(self.i2c)
        super().__init__(self.sensor_type)

    def get_data(self) -> SensorData:
        with self.i2c_lock:
            res = [self.mpu.gyro]
        return SensorData(self.id, self.sensor_type, res)


class DebugGyroSensor(Sensor):
    def __init__(self, _id: int, port: str, baudrate: int):
        self.id = _id
        self.sensor_type = SensorType.GYRO
        self.port = port
        self.baudrate = baudrate
        self.logger = logging.getLogger("debug-gyro-sensor_" + str(_id))
        super().__init__(self.sensor_type)

    def get_data(self) -> SensorData:
        with serial.Serial(self.port, self.baudrate, timeout=1, stopbits=2) as ser:
            res = {}
            while True:
                try:
                    data = ser.readline().decode("utf-8")
                    res = json.loads(json.loads(data)["gyro"])
                except Exception as e:
                    self.logger.warning(f"Could not decode on sensor {self.id} - retrying")
                    continue
                break
        return SensorData(self.id, self.sensor_type, res)


if __name__ == '__main__':
    s = GyroSensor(1, Lock())
    print(s.get_data())
