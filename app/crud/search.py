from app.database.mongo import mongo_db
from bson import ObjectId
from datetime import datetime

collection = mongo_db["search_history"]

def save_search(payload):
    doc = {
        "user_uid": payload.user_uid,
        "description": payload.data.description,
        "lat": payload.data.lat,
        "lng": payload.data.lng,
        "distance": payload.data.distance,
        "created_at": datetime.utcnow()
    }
    result = collection.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc


def get_user_searches(user_uid: str, limit: int = 10):
    cursor = (
        collection
        .find({"user_uid": user_uid})
        .sort("created_at", -1)
        .limit(limit)
    )

    results = []
    for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        results.append(doc)

    return results
