from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from app.crud import get_top_scores, insert_score, update_score, delete_score
from typing import Annotated, Union, Dict
from app.database import get_database
from app.models import Score, ScoreDB
from app.load_csv import load_scores_from_file
from app.auth import authenticate
from dotenv import load_dotenv
import uuid
import os
import logging

app = FastAPI(
    title="Gaming Service",
    description="API for managing top scores in the gaming service.",
    version="1.0.0",
    docs_url="/docs"
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
db = get_database()
score_collection = db.get_collection("scores")

@app.post('/login', response_model=Dict)
def login(
        payload: OAuth2PasswordRequestForm = Depends()
    ):
    """Processes user's authentication and returns a token
    on successful authentication.

    request body:

    - username: Unique identifier for a user e.g email, 
                phone number, name

    - password:
    """
    try:
        assert payload.username
        assert payload.username in os.getenv("USERS")
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    return {
        "access_token": payload.username
    }

@app.post("/load-scores/", response_model=Dict)
async def load_scores(token: Annotated[Union[str, None], Header()] = None):
    authenticate(token)
    await load_scores_from_file(score_collection)
    return {"message": "Scores loaded successfully from file."}


@app.get("/top-scores/", response_model=list[ScoreDB])
async def read_top_scores(token: Annotated[Union[str, None], Header()] = None):
    authenticate(token)
    top_scores = await get_top_scores(score_collection)
    return top_scores

@app.post("/scores/", response_model=ScoreDB)
async def create_score(score: Score, 
                       token: Annotated[Union[str, None], Header()] = None
):
    authenticate(token)
    player_id = str(uuid.uuid4())
    score_db = ScoreDB(**score.dict())
    score_db.id = player_id
    await insert_score(score_collection, score_db)
    return score_db

@app.put("/scores/{score_id}", response_model=ScoreDB)
async def update_scores(score_id: str, 
                       score: Score, 
                       token: Annotated[Union[str, None], Header()] = None
):
    authenticate(token)
    score_db = ScoreDB(**score.dict())
    score_db.id = score_id
    success = await update_score(score_collection, score_id, score)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Score not found")
    return score_db

@app.delete("/scores/{score_id}", response_model=Dict)
async def delete_scores(score_id: str, 
                       token: Annotated[Union[str, None], Header()] = None
):
    authenticate(token)
    success = await delete_score(score_collection, score_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Score not found")
    return {"message": "Score deleted successfully"}