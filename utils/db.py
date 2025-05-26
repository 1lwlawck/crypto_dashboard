from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("MONGO_USERNAME")
pwd = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")
params = os.getenv("MONGO_PARAMS")

def get_mongo_connection():
    uri = f"mongodb+srv://{user}:{pwd}@{cluster}/?{params}"
    return MongoClient(uri)

def get_collection():
    client = get_mongo_connection()
    db_name = os.getenv("DATABASE_NAME")
    col_name = os.getenv("COLLECTION_NAME")
    return client[db_name][col_name]
