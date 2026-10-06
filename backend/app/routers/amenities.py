from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Amenity

router = APIRouter(prefix="/amenities", tags=["Amenities"])

@router.get("")
def get_amenities(db: Session = Depends(get_db)):
    return [{"id": a.id, "name": a.name} for a in db.query(Amenity).order_by(Amenity.name).all()]
