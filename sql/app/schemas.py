from pydantic import BaseModel
from typing import Optional

class PlayerBase(BaseModel):
    birthYear: Optional[float]
    birthMonth: Optional[float]
    birthDay: Optional[float]
    birthCountry: Optional[str]
    birthState: Optional[str]
    birthCity: Optional[str]
    deathYear: Optional[float]
    deathMonth: Optional[float]
    deathDay: Optional[float]
    nameFirst: str
    nameLast: str
    nameGiven: Optional[str]
    weight: Optional[float]
    height: Optional[float]
    bats: Optional[str]
    throws: Optional[str]
    debut: Optional[str]
    finalGame: Optional[str]
    retroID: Optional[str]
    bbrefID: Optional[str]


class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    playerID: str

    class Config:
        orm_mode = True