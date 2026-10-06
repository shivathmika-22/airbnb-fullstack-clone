from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Booking, Listing
from app.schemas import BookingCreate, BookingOut
from app.dependencies.auth import get_current_user
from app.services.bookings import create_booking

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("", response_model=BookingOut, status_code=201)
def book(payload: BookingCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    listing = db.get(Listing, payload.listing_id)
    if not listing:
        raise HTTPException(404, "Listing not found")
    if payload.check_in < date.today():
        raise HTTPException(400, "Check-in cannot be in the past")
    return create_booking(db, listing, user.id, payload.check_in, payload.check_out, payload.guests)

@router.get("", response_model=list[BookingOut])
def my_bookings(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Booking).filter(Booking.guest_id == user.id).order_by(Booking.check_in.desc()).all()

@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.guest_id != user.id and booking.listing.host_id != user.id:
        raise HTTPException(403, "Not authorized")
    return booking

@router.post("/{booking_id}/cancel", response_model=BookingOut)
def cancel_booking(booking_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.guest_id != user.id:
        raise HTTPException(403, "Only the guest can cancel this booking")
    if booking.status == "cancelled":
        return booking
    booking.status = "cancelled"
    booking.cancelled_at = datetime.utcnow()
    db.commit()
    db.refresh(booking)
    return booking
