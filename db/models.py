from dataclasses import dataclass
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Integer, String, Float, Boolean, ForeignKey, create_engine
from datetime import datetime
from typing import List
from threading import Thread

class CanSatDB:
    def __init__(self, db_path: str) -> None:
        self.engine = None
        self.initialized = False
        self.db_path = db_path

    def init(self):
        self.engine = create_engine(self.db_path, echo=True)
        self.initialized = True

class CanSatDBService(Thread):
    pass

class Base(DeclarativeBase):
    pass


@dataclass
class BaseSensorData(Base):
    __tablename__ = 'base_sensor_data'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    time: Mapped[datetime] = mapped_column(DateTime)
    sensor_id: Mapped[int] = mapped_column(Integer)
    data_id: Mapped[str] = mapped_column(String)
    sensor_type: Mapped[str] = mapped_column(String)
    d1: Mapped[float] = mapped_column(Float, nullable=True)
    d2: Mapped[float] = mapped_column(Float, nullable=True)
    d3: Mapped[float] = mapped_column(Float, nullable=True)

    session_id: Mapped[int] = mapped_column(ForeignKey("cansat_sessions.id"))
    session: Mapped["CanSatSession"] = relationship(back_populates="sensor_data")


@dataclass
class CanSatSession(Base):
    __tablename__ = 'cansat_session'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    debug: Mapped[bool] = mapped_column(Boolean, default=False)
    creation_time: Mapped[datetime] = mapped_column(DateTime)
    sensor_data: Mapped[List["BaseSensorData"]] = relationship(back_populates="session")
