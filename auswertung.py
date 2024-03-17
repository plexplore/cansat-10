import datetime
import os
import sqlite3
from dateutil import parser
import numpy as np
import matplotlib.pyplot as plt

DIR = "auswertung"
DB_FILE = "data.sql"


class BaseData:
    def __init__(self, _id, time, value):
        self.id = _id
        self.time = parser.parse(time)
        self.value1 = value


class Auswertung:
    def __init__(self):
        self.raw_temp: list[BaseData] = []
        self.raw_pressure: list[BaseData] = []
        os.makedirs(DIR, exist_ok=True)
        os.removedirs(DIR)
        os.makedirs(DIR, exist_ok=True)

        self.db = sqlite3.connect(DB_FILE)
        self.cursor = self.db.cursor()
        self.data_beginn = parser.parse("2024-03-13 12:11:10")
        self.data_end = parser.parse("2024-03-13 12:12:22")

    def prepare_data(self):
        self.cursor.execute("SELECT * FROM base_sensor_data")
        data = self.cursor.fetchall()

        for i in data:
            d = BaseData(i[0], i[1], i[5])
            if d.time > self.data_beginn and d.time < self.data_end:
                if i[4] == "SensorType.TEMPERATURE_BMP180":
                    self.raw_temp.append(d)
                elif i[4] == "SensorType.PRESSURE":
                    self.raw_pressure.append(d)

    def run(self):
        self.prepare_data()
        fig1, ax1 = plt.subplots()
        fig1.dpi = 300
        self.calc_hoehe = [(44330 * (1 - ((i.value1 / 1012) ** (1 / 5.255)))) for i in self.raw_pressure]
        self.calc_hoehe2 = [((pow((1012.78 / p.value1), (1.0 / 5.257)) - 1) * ((t.value1) + 273.15)) / 0.0065
                            for t, p in zip(self.raw_temp, self.raw_pressure)]
        ax1.plot([(i.time - self.data_beginn).total_seconds() for i in self.raw_pressure],
                 self.calc_hoehe, color="tab:orange")

        ax1.plot([(i.time - self.data_beginn).total_seconds() for i in self.raw_pressure],
                 self.calc_hoehe2, color="tab:red")

        d1 = []

        t1 = []
        for t, i in zip(self.raw_pressure, self.calc_hoehe):
            if self.data_beginn + datetime.timedelta(seconds=25) < t.time < self.data_beginn + datetime.timedelta(
                    seconds=60):
                d1.append(i)
                t1.append(t)

        m, b = np.polyfit([(i.time - self.data_beginn).total_seconds() for i in t1], d1, 1)
        print(m, b)

        poly1d_fn = np.poly1d((m, b))
        ax1.plot([(i.time - self.data_beginn).total_seconds() for i in t1],
                 poly1d_fn([(i.time - self.data_beginn).total_seconds() for i in t1]), linestyle="--", color="cyan",
                 linewidth=4)

        # ax1.plot([(i.time - self.data_beginn).total_seconds() for i in self.raw_temp], [i.value1 for i in
        # self.raw_temp], color="tab:orange")
        ax1.set_xlabel("Zeit in Sekunden")
        ax1.set_ylabel("Höhe in m", color="tab:orange")
        ax2 = ax1.twinx()

        ax2.plot([(i.time - self.data_beginn).total_seconds() for i in self.raw_pressure],
                 [i.value1 for i in self.raw_pressure], color="tab:blue")
        ax2.set_ylabel("Druck in mBar", color="tab:blue")

        plt.show()
        print(max(self.calc_hoehe2))
        print(max(self.calc_hoehe))
        time_w = 18
        for i in range(len(self.raw_pressure)):
            if time_w < (self.raw_pressure[i].time - self.data_beginn).total_seconds():
                print(self.calc_hoehe[i])
                break


if __name__ == '__main__':
    Auswertung().run()
