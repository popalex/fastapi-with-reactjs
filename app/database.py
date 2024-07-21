from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from environment variables
MONGO_DETAILS = os.getenv('MONGO_DETAILS', 'mongodb://127.0.0.1:27017')

print(f"Got MONGO_DETAILS {MONGO_DETAILS}")

client = AsyncIOMotorClient(MONGO_DETAILS)

def get_database():
    return client.get_database("database_name")
