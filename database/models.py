from sqlalchemy import create_engine, Column, Integer, Boolean, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


engine = create_engine("sqlite:///database/database.db")
Session = sessionmaker(engine)
session = Session()

Base = declarative_base()


class Users(Base):
    """
    Represents a user in the system.

    Each user has a unique name and is associated with a Settings object
    that stores their preferences and configuration.

    Attributes:
        id (int): Unique identifier for the user (auto-incremented).
        name (str): Unique name of the user. Cannot be null.
        settings_id (int): Foreign key linking to the user's settings.
        settings (Settings): Relationship to the associated Settings object.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)
    settings_id = Column(Integer, ForeignKey("settings.id"), nullable=False)

    settings = relationship("Settings", back_populates="users", cascade="all")

    def to_json(self):
        """
        Serializes the user object to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary mapping column names to their values.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Settings(Base):
    """
    Represents user-specific configuration settings.

    This includes preferences such as timeframes, exchanges, language, and trading symbols.

    Attributes:
        id (int): Unique identifier for the settings record (auto-incremented).
        oi_timeframe (str): Default timeframe for open interest data (default: '5min').
        exchanges (list): List of exchanges the user follows (default: ['Bybit']).
        language (str): User's preferred language (default: 'English').
        symbols (list): List of trading symbols (default: empty list).
        users (Users): Relationship to the associated User object.
    """
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    oi_timeframe = Column(Text, nullable=False, default="5min")
    exchanges = Column(JSON, nullable=False, default=['Bybit'])
    language = Column(Text, nullable=False, default="English")
    symbols = Column(JSON, nullable=True, default=[])

    users = relationship("Users", back_populates="settings", cascade="all")

    def to_json(self):
        """
        Serializes the user object to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary mapping column names to their values.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
