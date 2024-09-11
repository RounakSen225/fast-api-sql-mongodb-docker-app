import csv
from .models import Player
from .database import SessionLocal
import pathlib

# Utility function to convert empty strings to None for numeric fields
def safe_float(value):
    try:
        return float(value) if value.strip() != '' else None
    except ValueError:
        return None

def load_data_from_csv():
    # Path to the uploaded CSV file
    csv_file_path = str(pathlib.Path(__file__).parent.resolve()) + '/player.csv'

    # Create a new database session
    db = SessionLocal()
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Create a Player object for each row in the CSV, converting empty strings to None
                player = Player(
                    playerID=row['playerID'],
                    birthYear=safe_float(row['birthYear']),
                    birthMonth=safe_float(row['birthMonth']),
                    birthDay=safe_float(row['birthDay']),
                    birthCountry=row['birthCountry'] or None,
                    birthState=row['birthState'] or None,
                    birthCity=row['birthCity'] or None,
                    deathYear=safe_float(row['deathYear']),
                    deathMonth=safe_float(row['deathMonth']),
                    deathDay=safe_float(row['deathDay']),
                    nameFirst=row['nameFirst'],
                    nameLast=row['nameLast'],
                    nameGiven=row['nameGiven'] or None,
                    weight=safe_float(row['weight']),
                    height=safe_float(row['height']),
                    bats=row['bats'] or None,
                    throws=row['throws'] or None,
                    debut=row['debut'] or None,
                    finalGame=row['finalGame'] or None,
                    retroID=row['retroID'] or None,
                    bbrefID=row['bbrefID'] or None
                )
                db.merge(player)  # Use merge to handle duplicates
            db.commit()
    except Exception as e:
        print(f"Error loading data from CSV: {e}")
        db.rollback()
    finally:
        db.close()