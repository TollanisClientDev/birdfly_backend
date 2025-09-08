from fastapi import APIRouter, HTTPException
from app.database.mongo import trip_logs_collection
from app.schemas_mongo.trip_log import TripLogCreate, TripLogAppend
from bson import ObjectId

router = APIRouter()

@router.post("/")
def create_trip_log(log: TripLogCreate):
    data = log.dict()
    result = trip_logs_collection.insert_one(data)
    return {"inserted_id": str(result.inserted_id)}

@router.put("/append")
def append_to_trip_log(data: TripLogAppend):
    result = trip_logs_collection.update_one(
        {"trip_id": data.trip_id},
        {"$push": {"route": data.new_point.dict()}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Trip log not found")
    return {"message": "GPS point added."}

@router.get("/{trip_id}")
def get_trip_log(trip_id: int):
    log = trip_logs_collection.find_one({"trip_id": trip_id})
    if not log:
        raise HTTPException(status_code=404, detail="Trip log not found")
    log["_id"] = str(log["_id"])  # Convert ObjectId to string
    return log
