from threading import Thread, Lock, Event
from models.sensor import Sensor, SensorData
import time


class SensorService(Thread):
    def __init__(self, sensor: Sensor, data: list[SensorData], data_lock: Lock, ex_e: Event, rq_per_sec=5):
        super(SensorService, self).__init__()
        self.sensor = sensor
        self.data = data
        self.data_lock = data_lock
        self.rq_per_sec = rq_per_sec
        self.ex_e = ex_e

    def run(self):
        t = 0.0
        while not self.ex_e.wait(timeout=t):
            ts = time.time()
            sd = self.sensor.get_data()
            with self.data_lock:
                self.data.append(sd)
            t = max(0.0, (1 / self.rq_per_sec) - (time.time() - ts))

"""if __name__ == '__main__':
    import RPi.GPIO as GPIO
    import time

    servoPIN = 12
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    p.start(12) # Initialisierung
    time.sleep(2)
    p.ChangeDutyCycle(7.4)

    p.stop()
    GPIO.cleanup()"""

"""if __name__ == '__main__':
    import time
    import busio
    from digitalio import DigitalInOut, Direction, Pull
    import board
    import adafruit_rfm9x

    CS = DigitalInOut(board.CE1)
    RESET = DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868)

    rfm9x.send(bytes("Hello World!", "utf-8"))
    rfm9x.max_power"""


if __name__ == '__main__':
    from pyLoraRFM9x import LoRa, ModemConfig

# This is our callback function that runs when a message is received
    def on_recv(payload):
        print("From:", payload.header_from)
        print("Received:", payload.message)
        print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))

    # Use chip select 1. GPIO pin 5 will be used for interrupts and set reset pin to 25
    # The address of this device will be set to 2
    lora = LoRa(1, 5, 2, reset_pin = 25, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=14, acks=True)
    lora.on_recv = on_recv

    # Send a message to a recipient device with address 10
    # Retry sending the message twice if we don't get an  acknowledgment from the recipient
    message = "Hello there!"
    status = lora.send_to_wait(message, 10, retries=2)
    if status is True:
        print("Message sent!")
    else:
        print("No acknowledgment from recipient")


