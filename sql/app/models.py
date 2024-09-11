from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class Player(Base):
    __tablename__ = "players"

    playerID = Column(String, primary_key=True, index=True, unique=True)
    birthYear = Column(Float, nullable=True)
    birthMonth = Column(Float, nullable=True)
    birthDay = Column(Float, nullable=True)
    birthCountry = Column(String)
    birthState = Column(String)
    birthCity = Column(String)
    deathYear = Column(Float, nullable=True)
    deathMonth = Column(Float, nullable=True)
    deathDay = Column(Float, nullable=True)
    nameFirst = Column(String)
    nameLast = Column(String)
    nameGiven = Column(String)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    bats = Column(String)
    throws = Column(String)
    debut = Column(String)  # Storing as a string to simplify (alternatively Date type can be used)
    finalGame = Column(String)  # Storing as a string to simplify (alternatively Date type can be used)
    retroID = Column(String)
    bbrefID = Column(String)