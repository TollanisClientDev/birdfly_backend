from fastapi import APIRouter, Depends
from app.schemas.search import SearchCreate, SearchOut
from app.crud.search import save_search, get_user_searches
from typing import List

router = APIRouter(prefix="/search_history", tags=["Search"])

@router.post("/", response_model=SearchOut)
def save_user_search(payload: SearchCreate):
    saved = save_search(payload)
    return saved

@router.get("/{user_uid}", response_model=List[SearchOut])
def get_search_list(user_uid: str, limit: int = 10):
    return get_user_searches(user_uid, limit)
