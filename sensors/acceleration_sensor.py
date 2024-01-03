import json
import logging

import serial

from models.sensor import Sensor, SensorType, SensorData
class DebugAccelerationSensor(Sensor):
    def __init__(self, _id: int, port: str, baudrate: int):
        self.id = _id
        self.sensor_type = SensorType.ACCELERATION
        self.port = port
        self.baudrate = baudrate
        self.logger = logging.getLogger("debug-acceleration-sensor_" + str(_id))
        super().__init__(self.sensor_type)

    def get_data(self) -> SensorData:
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