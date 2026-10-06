from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

def get_current_user(x_user_id: int | None = Header(default=None), db: Session = Depends(get_db)):
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="X-User-Id header is required")
    user = db.get(User, x_user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user

def require_host(user=Depends(get_current_user)):
    if user.role != "host":
        raise HTTPException(status_code=403, detail="Host access required")
    return user
