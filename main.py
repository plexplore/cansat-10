#!/bin/python3
import logging
import math
import os.path
import sys
import argparse
from sensors.dummy import DummySensor
from sensors.acceleration_sensor import DebugAccelerationSensor, AccelerationSensor#
from sensors.pressure import PressureSensor
from sensors.temperature import TemperatureBMP180Sensor
from sensors.gyrosensor import DebugGyroSensor, GyroSensor
from services.sensor import SensorService
from db.service import CanSatDB
import models.sensor as _sensor
import globals as g
import atexit
from threading import Event, Thread, Lock
import yaml
import time
from models.beeper import *
import RPi.GPIO as GPIO
import  picamera

class CanSat:
    debug: bool = False
    logger = logging.getLogger("cansat-main")
    cs_sensors: list[Thread] = []
    data: list[_sensor.SensorData] = []
    send_data: list[_sensor.SensorData] = []
    save_data: list[_sensor.SensorData] = []
    ram_data = {
        _sensor.SensorType.GYRO: [],
        _sensor.SensorType.PRESSURE: [],
        _sensor.SensorType.TEMPERATURE_BMP180: [],
        _sensor.SensorType.ACCELERATION: [],
    }
    data_lock = Lock()
    i2c_lock = Lock()

    last_min_acc = 0
    last_max_acc = 0
    last_extreme_acc_time = time.time()

    args = {}
    conf = {}

    beep = Beeper()



    def __init__(self):
        self.exit_event = Event()
        self.exit_send_and_save = Event()
        self.db = CanSatDB()

    def prepare_data(self):
        with self.data_lock:
            self.send_data.extend(self.data)
            self.save_data.extend(self.data)
            for i in self.data:
                self.ram_data[i.sensor_type].append(i)
            self.data.clear()

    def exit_handler(self):
        if not self.exit_event.is_set():
            self.logger.info("Wants exit, setting Event...")
            self.exit_event.set()
            for sensor in self.cs_sensors:
                sensor.join()
            self.prepare_data()
            GPIO.cleanup()
            self.exit_send_and_save.set()

    def init_logging(self):
        try:
            if not self.debug:
                logging.basicConfig(filename=g.LOG_FILE, level=logging.INFO)
                log = logging.getLogger()
                log.addHandler(logging.StreamHandler(sys.stdout))
            else:
                logging.basicConfig(level=logging.DEBUG)

        except Exception as e:
            self.logger.critical("!!!Failed to initialize logging!!!")
            self.logger.critical(e)

    def parse_args(self):
        parser = argparse.ArgumentParser(g.PROGRAMM)
        parser.add_argument("--debugging", action="store_true", default=False)

        self.args = parser.parse_args()
        self.debug = self.args.debugging

    def setup_conf(self):
        with open(g.get_conf_path(self.debug)) as c:
            self.conf = yaml.safe_load(c.read())

    def init(self):
        atexit.register(self.exit_handler)
        self.parse_args()
        # make dirs
        os.makedirs(g.DATA_DIR, exist_ok=True)
        os.makedirs(g.LOG_DIR, exist_ok=True)
        self.init_logging()
        self.setup_conf()
        self.db.init(self.conf["db"], self.exit_send_and_save, self.save_data, self.data_lock, self.debug)
        self.logger.info("Running with args: %s", self.args)
        self.logger.info("And with conf: %s", self.conf)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)

        self.servo1 = GPIO.PWM(12, 50)
        self.servo2 = GPIO.PWM(13, 50)






        self.logger.info("CanSat successfully initialized")

    def make_sensor_service(self, sensor: _sensor.Sensor) -> SensorService:
        return SensorService(sensor, self.data, self.data_lock, self.exit_event)

    def setup_sensor(self, id: int, conf: dict) -> SensorService:
        k, v = next(iter(conf.items()))
        st = _sensor.get_sensor_type(k)
        conf = v
        if conf["type"].lower() == "usbserial":
            if st == _sensor.SensorType.ACCELERATION:
                return self.make_sensor_service(DebugAccelerationSensor(id, conf["port"], conf["baud"]))
            elif st == _sensor.SensorType.GYRO:
                return self.make_sensor_service(DebugGyroSensor(id, conf["port"], conf["baud"]))

        self.logger.warning(f"Sensor type for {id} not implemented, using dummy")
        return self.make_sensor_service(DummySensor(id))

    def setup_sensors(self):
        #self.cs_sensors.append(self.make_sensor_service(GyroSensor(1, self.i2c_lock,)))
        #self.cs_sensors.append(self.make_sensor_service(AccelerationSensor(2, self.i2c_lock,)))
        self.cs_sensors.append(self.make_sensor_service(TemperatureBMP180Sensor(3, self.i2c_lock,)))
        self.cs_sensors.append(self.make_sensor_service(PressureSensor(4, self.i2c_lock,)))

        for i in self.cs_sensors:
            i.start()

        """for i, s in enumerate(self.conf["sensors"]):
            ss = self.setup_sensor(i, s)
            ss.start()
            self.cs_sensors.append(ss)"""

    def startup(self):
        self.setup_sensors()
        self.db.service.start()

    def check_status(self):
        res_bschl = []
        for i in self.ram_data[_sensor.SensorType.ACCELERATION]:
            res_bschl.append(math.sqrt(i[0]**2 + i[1]**2 + i[2]**2))

        ma = max(res_bschl)
        mi = min(res_bschl)

        if not (self.last_max_acc == ma and self.last_min_acc == mi):
            self.last_max_acc = ma
            self.last_min_acc = mi
            self.last_extreme_acc_time = time.time()
        else:
            print("no max acc for: " + str((time.time() - self.last_extreme_acc_time)))




    def run(self):
        self.init()
        try:
            self.startup()


            self.servo1.start(0)
            self.servo2.start(0)
    
            self.servo1.ChangeDutyCycle(9.3)
            self.servo2.ChangeDutyCycle(5.3)
    
            time.sleep(60)
    
            self.servo1.ChangeDutyCycle(7.3)
            self.servo2.ChangeDutyCycle(7.3)
    
            self.servo1.stop()
            self.servo2.stop()

            self.logger.info("Ready - waiting for exit...")
            t = time.time()
            #c = picamera.PiCamera()
            #c.resolution = (2592,1944)
            #c.start_preview()

            while not self.exit_event.wait(timeout=0.5):
                #self.check_status()
                self.prepare_data()
                #if time.time() - t > 10:
                 #   t=time.time()
                    #c.capture("/home/pi/cansat/data/" + str(time.time())+ ".jpg")


                   # self.logger.info("take picture")
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                self.logger.info("KeyboardInterrupt -> exiting...")
                self.exit_handler()
            else:
                self.logger.critical("!!!Main-Thread crashed... Others continuing...!!!")
                self.logger.critical(e)


cansat = CanSat()

if __name__ == '__main__':
    cansat.run()
