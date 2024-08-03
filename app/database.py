import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from environment variables
MONGO_DETAILS = os.getenv('MONGO_DETAILS', 'mongodb://127.0.0.1:27017')

print(f"Got MONGO_DETAILS {MONGO_DETAILS}")

client = AsyncIOMotorClient(MONGO_DETAILS)

def get_database():
    return client.get_database("database_name")
