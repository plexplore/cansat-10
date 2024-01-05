from db.db_models import Base, CanSatSession, BaseSensorData
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Engine
from datetime import datetime
from threading import Thread, Event, Lock
from models.sensor import SensorData
import logging


class CanSatDB:
    def __init__(self) -> None:
        self.service = None
        self.engine = None
        self.initialized = False
        self.db_path = None

    def init(self, db_path: str, ee: Event, data: list[SensorData], lock: Lock, debug: bool = False) -> CanSatSession:
        self.db_path = db_path
        self.engine = create_engine(self.db_path, echo=False)
        Base.metadata.create_all(self.engine)
        cs = self.create_cansat_session(debug=debug)
        self.service = CanSatDBService(self.engine, cs, ee, data, lock)
        self.initialized = True
        return cs

    def create_cansat_session(self, debug: bool = False) -> CanSatSession:
        with Session(self.engine) as db:
            s = CanSatSession(debug=debug, creation_time=datetime.now())
            db.add(s)
            db.commit()
        return s


class CanSatDBService(Thread):
    def __init__(self, engine: Engine, session: CanSatSession, exit_event: Event, sensor_data: list[SensorData],
                 data_lock: Lock) -> None:
        super(CanSatDBService, self).__init__()
        self.logger = logging.getLogger("db")
        self.engine = engine
        self.session = session
        self.exit_event = exit_event
        self.sensor_data = sensor_data
        self.data_lock = data_lock

    def run(self) -> None:
        self.logger.info("Starting CanSatDBService")
        while not (self.exit_event.wait(timeout=1) and len(self.sensor_data) == 0):
            try:
                with self.data_lock:
                    t: list[SensorData] = self.sensor_data.copy()
                    print(len(self.sensor_data))
                    self.sensor_data.clear()
                bsd: list[BaseSensorData] = []
                for i in t:
                    bsd.append(i.to_base_sensor_data(self.session))
                with Session(self.engine) as s:
                    s.add_all(bsd)
                    s.commit()
                    self.logger.info("saved")

            except Exception as e:
                self.logger.error("Failed to save data", exc_info=e)

        self.logger.info("Finished CanSatDBService with entries: " + str(len(self.sensor_data)))
