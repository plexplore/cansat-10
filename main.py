#!/bin/python3
import logging
import os.path
import sys
import argparse
import models.sensor
import constants


class CanSat:
    debug: bool = False
    logger = logging.getLogger("cansat-main")

    def __init__(self):
        pass

    def init_logging(self):
        try:
            if not self.debug:
                logging.basicConfig(filename=constants.LOG_FILE, level=logging.INFO)
                log = logging.getLogger()
                log.addHandler(logging.StreamHandler(sys.stdout))
            else:
                logging.basicConfig(level=logging.DEBUG)

        except Exception as e:
            self.logger.critical("!!!Failed to initialize logging!!!")
            self.logger.critical(e)

    def parse_args(self):
        parser = argparse.ArgumentParser(constants.PROGRAMM)
        parser.add_argument("--debugging", action="store_true", default=False)

        constants.args = parser.parse_args()
        self.debug = constants.args.debugging

    def init(self):
        try:
            self.parse_args()
            # make dirs
            os.makedirs(constants.DATA_DIR, exist_ok=True)
            os.makedirs(constants.LOG_DIR, exist_ok=True)
            self.init_logging()

            self.logger.info("Running with: %s", constants.args)
            self.logger.info("CanSat successfully initialized")
        except Exception as e:
            self.logger.critical("!!!Initialization failed!!!")
            self.logger.critical(e)

    def run(self):
        try:
            self.init()
        except Exception as e:
            self.logger.critical("!!!Main-Thread crashed... Others continuing...!!!")
            self.logger.critical(e)


cansat = CanSat()

if __name__ == '__main__':
    cansat.run()
