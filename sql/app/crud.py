from sqlalchemy.orm import Session
import uuid
from . import models, schemas

def get_players(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Player).offset(skip).limit(limit).all()

def get_player_by_id(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.playerID == player_id).first()

def create_player(db: Session, player: schemas.PlayerCreate):
    player_id = str(uuid.uuid4())
    db_player = models.Player(playerID = player_id, **player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def update_player(db: Session, player: schemas.PlayerCreate, player_id: int):
    db_player = db.query(models.Player).filter(models.Player.playerID == player_id).first()
    if db_player:
        for key, value in player.dict().items():
            setattr(db_player, key, value)
        db.commit()
        db.refresh(db_player)
    return db_player

def delete_player(db: Session, player_id: int):
    db_player = db.query(models.Player).filter(models.Player.playerID == player_id).first()
    if db_player:
        db.delete(db_player)
        db.commit()
    return db_player