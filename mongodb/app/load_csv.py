from app.models import ScoreDB
import logging
import csv
from pymongo import collection
import pathlib

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def load_scores_from_file(score_collection: collection.Collection):
    file_path = str(pathlib.Path(__file__).parent.resolve()) + '/players.csv'
    logger.info(f"Loading scores from file: {file_path}")

    # Read the CSV file
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        scores_to_insert = []
        for row in reader:
            score_db = ScoreDB(player_name=row['player_name'], score=int(row['score']))
            scores_to_insert.append(score_db.dict(by_alias=True))
        
        # Insert all scores into the database in one bulk operation
        if scores_to_insert:
            result = await score_collection.insert_many(scores_to_insert)
            logger.info(f"Inserted {len(result.inserted_ids)} scores into the database.")
        else:
            logger.info("No scores found to insert.")