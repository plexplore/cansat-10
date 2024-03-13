import datetime
import time
from threading import Thread
import logging
import adafruit_rfm9x
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
import busio
import board
import digitalio
import json
from db.db_models import BaseSensorData
from models.sensor import SensorData, CanSatSession


class Sender:
    def __init__(self) -> None:
        self.service = None

    def init(self, data, exit_event, data_lock) -> None:
        self.service = SenderService(data, exit_event, data_lock)
        self.service.start()

class SenderService(Thread):
    def __init__(self, data, exit_event, data_lock) -> None:
        super(SenderService, self).__init__()
        self.data = data
        self.logger = logging.getLogger('SenderService')
        self.exit_event = exit_event
        self.data_lock = data_lock

    def run(self) -> None:
        self.logger.info("Starting SenderService")
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        cs = digitalio.DigitalInOut(board.CE1)
        irq = digitalio.DigitalInOut(board.D5)
        rst = digitalio.DigitalInOut(board.D25)
        s1 = bytearray()
        s2 = bytearray()
        s3 = bytearray()
        s1.extend(map(ord, "018229BB"))
        s2.extend(map(ord, "BFF2CA2C7191F895365CCF822C3224D1"))
        s3.extend(map(ord, "2541B4A7145935927393358617651B9B"))

        ttn_config = TTN(s1, s3, s2, country="DE")
        lora = TinyLoRa(spi, cs, irq, rst, ttn_config)



        while not (self.exit_event.wait(timeout=1) and len(self.data) == 0):
            with self.data_lock:
                t: list[SensorData] = self.data.copy()
                print(len(self.data))
                self.data.clear()
            bsd: list[dict] = []

            for i in t:
                bsd.append(i.to_base_sensor_data(CanSatSession(id=1, debug=False, creation_time=datetime.datetime.now(), )).to_dict())

            d: bytearray = bytearray()
            d.extend(map(ord, json.dumps().encode("utf-8")))
            lora.send_data(d,len(d), lora.frame_counter)



