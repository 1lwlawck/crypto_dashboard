from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_mongo_connection():
    uri = os.getenv("MONGO_URI")
    return MongoClient(uri)

def get_collection():
    client = get_mongo_connection()
    db_name = os.getenv("DATABASE_NAME")
    col_name = os.getenv("COLLECTION_NAME")
    return client[db_name][col_name]
