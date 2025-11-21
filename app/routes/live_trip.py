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

@router.get("/uid/{uid}", summary="Get current trip status")
def get_live_trip_by_uid(uid: str):
    live_trip = live_trip_updates_collection.find_one({"user_uid": uid})
    if not live_trip:
        raise HTTPException(status_code=404, detail="Live trip data not found")
    live_trip["_id"] = str(live_trip["_id"])
    return live_trip

@router.get("/{trip_id}", summary="Get current trip status")
def get_live_trip(trip_id: int):
    doc = live_trip_updates_collection.find_one({"trip_id": trip_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Live trip data not found")
    doc["_id"] = str(doc["_id"])
    return doc
