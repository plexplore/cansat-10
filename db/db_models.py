from dataclasses import dataclass
from dataclasses_json import dataclass_json
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Integer, String, Float, Boolean, ForeignKey
from datetime import datetime
from typing import List


class Base(DeclarativeBase):
    pass


@dataclass
@dataclass_json
class CanSatSession(Base):
    __tablename__ = 'cansat_session'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    debug: Mapped[bool] = mapped_column(Boolean, default=False)
    creation_time: Mapped[datetime] = mapped_column(DateTime)
    sensor_data: Mapped[List["BaseSensorData"]] = relationship(back_populates="session")


@dataclass
@dataclass_json
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

    session_id: Mapped[int] = mapped_column(ForeignKey("cansat_session.id"))
    session: Mapped["CanSatSession"] = relationship(back_populates="sensor_data")

if __name__ == '__main__':
    print(BaseSensorData(id=1, time=datetime.now(), sensor_id=3, data_id="hisdf", sensor_type="sdfg").to_json())
