import time
from threading import Thread


class Manager(Thread):
    def __init__(self, q):
        Thread.__init__(self)
        self._q = q

    def run(self):
        while True:
            pass


if __name__ == '__main__':
    m = Manager()
    m.start()
