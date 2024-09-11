from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get MongoDB connection details from environment variables
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_URL = "mongodb+srv://rounaksen225:SUsau8xs6F7O8YGJ@cluster0.ifxvd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
COLLECTION = os.getenv("COLLECTION")

# Setup logging
def get_database():
    try:
        client = AsyncIOMotorClient(DATABASE_URL)
        database = client[DATABASE_NAME]
        logger.info(f"Connected to MongoDB database: {DATABASE_NAME}")
        return database
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise e
