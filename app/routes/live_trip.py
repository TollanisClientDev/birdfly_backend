from fastapi import APIRouter, HTTPException
from app.database.mongo import live_trip_updates_collection
from app.schemas_mongo.live_trip import LiveTripUpdate
from datetime import datetime

router = APIRouter()

@router.post("/", summary="Create or update trip status")
def create_or_update_trip_status(data: LiveTripUpdate):
    result = live_trip_updates_collection.update_one(
        {"trip_id": data.trip_id},
        {"$set": data.dict()},
        upsert=True  # create if not exist
    )
    return {"message": "Trip status updated."}

@router.get("/{trip_id}", summary="Get current trip status")
def get_trip_status(trip_id: int):
    doc = live_trip_updates_collection.find_one({"trip_id": trip_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Live trip data not found")
    doc["_id"] = str(doc["_id"])
    return doc
