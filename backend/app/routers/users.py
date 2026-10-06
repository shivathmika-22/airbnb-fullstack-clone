from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserOut
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id).all()

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user
