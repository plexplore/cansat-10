#!/bin/python3
import logging
import os.path
import sys
import argparse
from sensors.dummy import DummySensor
from sensors.acceleration_sensor import *
from sensors.gyrosensor import *
from services.sensor import SensorService
import models.sensor as _sensor
import globals as g
import atexit
from threading import Event, Thread, Lock
import yaml


class CanSat:
    debug: bool = False
    logger = logging.getLogger("cansat-main")
    cs_sensors: list[Thread] = []
    data: list[_sensor.SensorData] = []
    data_lock = Lock()
    args = {}
    conf = {}

    def __init__(self):
        self.exit_event = Event()

    def exit_handler(self):
        if not self.exit_event.is_set():
            self.logger.info("Wants exit, setting Event...")
            self.exit_event.set()

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
        try:
            atexit.register(self.exit_handler)
            self.parse_args()
            # make dirs
            os.makedirs(g.DATA_DIR, exist_ok=True)
            os.makedirs(g.LOG_DIR, exist_ok=True)
            self.init_logging()
            self.setup_conf()
            self.logger.info("Running with args: %s", self.args)
            self.logger.info("And with conf: %s", self.conf)
            self.logger.info("CanSat successfully initialized")
        except Exception as e:
            self.logger.critical("!!!Initialization failed!!!")
            self.logger.critical(e)

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
        for i, s in enumerate(self.conf["sensors"]):
            ss = self.setup_sensor(i, s)
            ss.start()
            self.cs_sensors.append(ss)

    def startup(self):
        self.setup_sensors()

    def run(self):
        try:
            self.init()
            self.startup()
            self.logger.info("Ready - waiting for exit...")
            while not self.exit_event.wait(timeout=0.1):
                pass
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
