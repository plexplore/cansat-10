#!/bin/python3
import logging
import os.path
import sys
import argparse
import time

import models.sensor
import globals as g
import atexit
from threading import Event

class CanSat:
    debug: bool = False
    logger = logging.getLogger("cansat-main")

    def __init__(self):
        self.exit_event = Event()

    def exit_handler(self):
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

        g.args = parser.parse_args()
        self.debug = g.args.debugging

    def init(self):
        try:
            atexit.register(self.exit_handler)
            self.parse_args()
            # make dirs
            os.makedirs(g.DATA_DIR, exist_ok=True)
            os.makedirs(g.LOG_DIR, exist_ok=True)
            self.init_logging()

            self.logger.info("Running with: %s", g.args)
            self.logger.info("CanSat successfully initialized")
        except Exception as e:
            self.logger.critical("!!!Initialization failed!!!")
            self.logger.critical(e)

    def startup(self):
        pass

    def run(self):
        try:
            self.init()
            self.startup()
            self.logger.info("Ready - waiting for exit...")
            self.exit_event.wait()
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
