import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.operations import SearchIndexModel
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import asyncio

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

    print("CSV Import Done!")

async def add_embeddings():
    db = get_database()
    items = db["database_name"]["items"].find()

    model = SentenceTransformer("all-MiniLM-L6-v2")

    for item in await items.to_list(1000):
        print(f"Got movie {item['Series_Title']}")
        embeddings = model.encode(item["Overview"], normalize_embeddings=True)
        item["plot_vect"] = embeddings
        item["Series_Title"] = item["Series_Title"] + "1"
        max_len = len(embeddings)
        db["database_name"]["items"].update_one(
            {"_id": item["_id"]},
            # {"$set": {'plot_vect': embeddings}}
            {"$set": item}
            )

    return max_len

def add_index(field_name: str, vector_length: int):
    db = get_database()

    # should "similarity" be "cosine"?

    search_model = SearchIndexModel(
    definition={
        "mappings": {
            "fields": [
                {
                    "type": "vector",
                    "path": field_name,
                    "numDimensions": vector_length,
                    "similarity": "dotProduct",
                }
            ],
        }
    },
    name="scenario_vector_index",
    )
    db["database_name"]["items"].create_search_index(search_model)
    print("Added search index !")

async def main():
    import_data()
    vect_lenght = await add_embeddings()
    add_index("plot_vect", vect_lenght)
    
if __name__ == '__main__':
    # See this for details:
    # https://stackoverflow.com/questions/50757497/simplest-async-await-example-possible-in-python
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())