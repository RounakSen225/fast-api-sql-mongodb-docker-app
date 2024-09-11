from app.models import ScoreDB, Score
from pymongo import DESCENDING, collection
import logging
from bson import ObjectId

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_top_scores(score_collection: collection.Collection, limit: int = 5) -> list:
    logger.info(f"Fetching top {limit} scores from the database")
    scores_cursor = score_collection.find().sort("score", DESCENDING).limit(limit)
    scores = await scores_cursor.to_list(length=limit)
    return [ScoreDB(**score) for score in scores]

async def insert_score(score_collection: collection.Collection, score: ScoreDB):
    logger.info(f"Inserting score: {score.player_name} with score {score.score}")
    result = await score_collection.insert_one(score.dict(by_alias=True))
    return str(result.inserted_id)

async def update_score(score_collection: collection.Collection, score_id: str, score: Score):
    logger.info(f"Updating score with ID: {score_id}")
    result = await score_collection.update_one(
        {"_id": score_id},
        {"$set": score.dict(by_alias=True)}
    )
    if result.modified_count == 1:
        return True
    return False

async def delete_score(score_collection: collection.Collection, score_id: str):
    logger.info(f"Deleting score with ID: {score_id}")
    result = await score_collection.delete_one({"_id": score_id})
    logger.info(result)
    if result.deleted_count == 1:
        return True
    return False