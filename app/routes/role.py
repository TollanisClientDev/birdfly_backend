from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.mysql import SessionLocal
from app.schemas.role import RoleCreate, RoleOut
from app.crud import role as role_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RoleOut)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return role_crud.create_role(db, role)

@router.get("/", response_model=list[RoleOut])
def get_roles(db: Session = Depends(get_db)):
    return role_crud.get_roles(db)
