from pydantic import BaseModel, Field, field_validator

# Pydantic model for input data validation
class ScoreCreate(BaseModel):
    player_name: str = Field(..., example="Player1")
    score: int = Field(..., example=1500)

    @field_validator('score')
    def check_score(cls, v):
        if v <= 0:
            raise ValueError("score has to be positive")
        return v

    class Config:
        orm_mode = True

# Pydantic model for MongoDB documents
class ScoreDB(ScoreCreate):
    id: str = Field(...,alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
