from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleCreate

def create_role(db: Session, role_data: RoleCreate):
    role = Role(**role_data.dict())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def get_roles(db: Session):
    return db.query(Role).all()
