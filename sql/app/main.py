from fastapi import FastAPI, Depends, HTTPException, Query, Header, status
from sqlalchemy.orm import Session
from . import models, schemas, crud
from typing import Annotated, Union, Dict
import logging
from dotenv import load_dotenv
from .auth import authenticate
from .database import engine, SessionLocal
from .load_csv import load_data_from_csv
from fastapi.security import OAuth2PasswordBearer
import os

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=engine)
load_dotenv()
#load_data_from_csv()

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi.security import OAuth2PasswordRequestForm

@app.post('/login', response_model=Dict)
def login(
        payload: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_db)
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

@app.get("/api/players", response_model=list[schemas.Player])
def get_players(
    db: Session = Depends(get_db),
    limit: int = Query(default=10, ge=1),
    offset: int = Query(default=0, ge=0),
    token: Annotated[Union[str, None], Header()] = None
):
    '''

    '''
    
    authenticate(token)
    logger.info("Fetching all players")
    players = crud.get_players(db, skip=offset, limit=limit)
    if players is None:
        logger.error(f"Players not found")
        raise HTTPException(status_code=404, detail="Players not found")
    return players

@app.get("/api/players/{player_id}", response_model=schemas.Player)
def get_player(player_id: str, 
               db: Session = Depends(get_db),
               token: Annotated[Union[str, None], Header()] = None
):
    authenticate(token)
    if not player_id or len(player_id) == 0:
        logger.error(f"Invalid player id")
        raise HTTPException(status_code=400, detail="Invalid Player")
    player = crud.get_player_by_id(db, player_id=player_id)
    if player is None:
        logger.error(f"Player with ID {player_id} not found")
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@app.post("/api/players/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, 
                  db: Session = Depends(get_db),
                  token: Annotated[Union[str, None], Header()] = None
):
    authenticate(token)
    if not player.nameFirst or player.nameFirst == "" or not player.nameLast or player.nameLast == "":
        logger.error(f"Invalid player")
        raise HTTPException(status_code=400, detail="Invalid Player")
    return crud.create_player(db=db, player=player)

@app.put("/api/players/{player_id}", response_model=schemas.Player)
def update_player(player_id: str, player: schemas.PlayerCreate, 
                  db: Session = Depends(get_db),
                  token: Annotated[Union[str, None], Header()] = None
):
    authenticate(token)
    if not player_id or len(player_id) == 0:
        logger.error(f"Invalid player id")
        raise HTTPException(status_code=400, detail="Invalid Player")
    db_player = crud.get_player_by_id(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.update_player(db=db, player=player, player_id=player_id)

@app.delete("/api/players/{player_id}", response_model=schemas.Player)
def delete_player(player_id: str, 
                  db: Session = Depends(get_db),
                  token: Annotated[Union[str, None], Header()] = None
):
    authenticate(token)
    if not player_id or len(player_id) == 0:
        logger.error(f"Invalid player id")
        raise HTTPException(status_code=400, detail="Invalid Player")
    db_player = crud.get_player_by_id(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.delete_player(db=db, player_id=player_id)