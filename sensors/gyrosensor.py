import json
import time

from models.sensor import Sensor, SensorType, SensorData
import serial


class DebugGyroSensor(Sensor):
    def __init__(self, _id: int, port: str, baudrate: int):
        self.id = _id
        self.sensor_type = SensorType.GYRO
        self.port = port
        self.baudrate = baudrate
        super().__init__(self.sensor_type)

    def get_data(self) -> SensorData:
        with serial.Serial(self.port, self.baudrate, timeout=1, stopbits=2) as ser:
            data = ser.readline().decode("utf-8")
            print(json.loads(data))
        return SensorData(self.id, self.sensor_type, data)

if __name__ == '__main__':
    s = DebugGyroSensor(1, "/dev/ttyACM0", 115200)
    s.get_data()