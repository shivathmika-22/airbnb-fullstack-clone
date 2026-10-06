from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Favorite, Listing
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.get("")
def favorites(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return [{"listing_id": x.listing_id} for x in db.query(Favorite).filter(Favorite.user_id == user.id).all()]

@router.post("/{listing_id}")
def add_favorite(listing_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not db.get(Listing, listing_id):
        raise HTTPException(404, "Listing not found")
    existing = db.query(Favorite).filter(Favorite.user_id == user.id, Favorite.listing_id == listing_id).first()
    if not existing:
        db.add(Favorite(user_id=user.id, listing_id=listing_id))
        db.commit()
    return {"listing_id": listing_id, "is_favorite": True}

@router.delete("/{listing_id}")
def remove_favorite(listing_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = db.query(Favorite).filter(Favorite.user_id == user.id, Favorite.listing_id == listing_id).first()
    if existing:
        db.delete(existing)
        db.commit()
    return {"listing_id": listing_id, "is_favorite": False}
