import board
import digitalio
from time import sleep

class Beeper:
    def __init__(self):
        self.pin = digitalio.DigitalInOut(board.D21)
        self.is_beeping = False
        self.beep_duration = 200
        self.beep_pause = 2

    def startup_beep(self):
        while self.is_beeping:
            sleep(0.001)
        self.is_beeping=True
        self.pin = True
        sleep(self.beep_duration/1000)
        self.pin = False
        self.is_beeping = False

    def sensor_error(self, _id:int):
        while self.is_beeping:
            sleep(0.001)
        self.is_beeping=True
        self.pin = True
        sleep(self.beep_duration/500)
        self.pin = False
        for i in range(_id):
            self.pin = True
            sleep(self.beep_duration/500)
            self.pin = False
        self.is_beeping = False

bee = Beeper()