from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

mongo_db = client["birdfly"]  # your MongoDB database
trip_logs_collection = mongo_db["trip_logs"]
live_trip_updates_collection = mongo_db["live_trip_updates"]