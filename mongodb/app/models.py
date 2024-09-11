from pydantic import BaseModel, Field, field_validator
from typing import List
from bson import ObjectId
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class Score(BaseModel):
    player_name: str
    score: int

    class Config:
        orm_mode = True

    @field_validator('score')
    def check_score(cls, v):
        if v <= 0:
            raise ValueError("score has to be positive")
        return v

# Define a schema for MongoDB documents
class ScoreDB(Score):
    id: str = Field(default_factory=lambda: "tmp", alias="_id")
