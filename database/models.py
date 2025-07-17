from sqlalchemy import create_engine, Column, Integer, Boolean, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


engine = create_engine("sqlite:///database.db")
Session = sessionmaker(engine)
session = Session()

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    settings_id = Column(Integer, ForeignKey("settings.id"))

    settings = relationship("Settings", back_populates="users", cascade="all")


class Settings(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    oi_timeframe = Column(Text, nullable=False, default="5min")
    exchanges = Column(JSON, nullable=False, default=['Bybit'])
    language = Column(Text, nullable=False, default="English")
    symbols = Column(JSON, nullable=True, default=[])

    users = relationship("Users", back_populates="settings", cascade="all")

