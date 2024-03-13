from PIL import Image
import datetime as dt
class Snapshot:
    def __init__(self):
        self.image = Image.open("")
        self.time = dt.datetime.now()
        pass

