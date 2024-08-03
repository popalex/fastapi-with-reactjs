import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.operations import SearchIndexModel
from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from environment variables
MONGO_DETAILS = os.getenv('MONGO_DETAILS', 'mongodb://127.0.0.1:27017')

print(f"Got MONGO_DETAILS {MONGO_DETAILS}")

client = AsyncIOMotorClient(MONGO_DETAILS)

def get_database():
    return client.get_database("database_name")

def import_data():
    data = pd.read_csv('csv/imdb_top_1000.csv').to_dict('records')
    db = get_database()
    
    db["database_name"]["items"].collection.delete_many({})
    db["database_name"]["items"].insert_many(data)

    print('Done!')

def add_embeddings():
    db = get_database()
    items = db["database_name"]["items"].find()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    print(model.max_seq_length)

    for item in items:
        print(f"Got item {item}")
        embeddings = model.encode(item["Overview"], normalize_embeddings=True)
        db["database_name"]["items"].update_one(
            {"_id": item["_id"]},
            {"$set": {'plot_vect': embeddings[0]}}
            )

    return model.max_seq_length

def add_index(field_name: str, vector_length: int):
    db = get_database()

    search_model = SearchIndexModel(
    definition={
        "mappings": {
            "fields": [
                {
                    "type": "vector",
                    "path": field_name,
                    "numDimensions": vector_length,
                    "similarity": "cosine",
                }
            ],
        }
    },
    name="scenario_vector_index",
    )
    db["database_name"]["items"].create_search_index(search_model)

def main():
    import_data()
    vect_lenght = add_embeddings()
    add_index("plot_vect", vect_lenght)
    
if __name__ == '__main__':
    main()