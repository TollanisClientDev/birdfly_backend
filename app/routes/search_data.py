from fastapi import APIRouter, HTTPException
from app.database.mongo import search_data_collection
from app.schemas_mongo.search_data import SearchDataCreate
from bson import ObjectId

router = APIRouter()

@router.post("/")
def save_search(data: SearchDataCreate):
    existing = search_data_collection.find_one({"user_id": data.user_id})
    if existing:
        search_data_collection.update_one(
            {"user_id": data.user_id},
            {"$push": {"searches": data.search.dict()}}
        )
    else:
        search_data_collection.insert_one({
            "user_id": data.user_id,
            "searches": [data.search.dict()]
        })
    return {"message": "Search saved"}

@router.get("/user/{user_id}")
def get_user_searches(user_id: int):
    data = search_data_collection.find_one({"user_id": user_id})
    if not data:
        raise HTTPException(status_code=404, detail="No search history")
    data["_id"] = str(data["_id"])
    return data

@router.delete("/user/{user_id}")
def delete_user_searches(user_id: int):
    result = search_data_collection.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="No search history to delete")
    return {"message": "Search history deleted"}
