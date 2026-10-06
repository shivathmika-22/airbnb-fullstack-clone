from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Review, Listing, Booking
from app.schemas import ReviewCreate, ReviewOut
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/listings/{listing_id}/reviews", tags=["Reviews"])

@router.get("", response_model=list[ReviewOut])
def list_reviews(listing_id: int, db: Session = Depends(get_db)):
    if not db.get(Listing, listing_id):
        raise HTTPException(404, "Listing not found")
    return db.query(Review).filter(Review.listing_id == listing_id).order_by(Review.created_at.desc()).all()

@router.post("", response_model=ReviewOut, status_code=201)
def create_review(listing_id: int, payload: ReviewCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not db.get(Listing, listing_id):
        raise HTTPException(404, "Listing not found")
    if db.query(Review).filter(Review.listing_id == listing_id, Review.user_id == user.id).first():
        raise HTTPException(409, "You already reviewed this listing")
    if not db.query(Booking).filter(
        Booking.listing_id == listing_id,
        Booking.guest_id == user.id,
        Booking.status == "confirmed"
    ).first():
        raise HTTPException(403, "Only guests with a booking can review")
    review = Review(listing_id=listing_id, user_id=user.id, rating=payload.rating, comment=payload.comment)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
