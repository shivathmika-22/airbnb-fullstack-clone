from fastapi import HTTPException
from app.models import Booking
from app.services.pricing import calculate_quote

def find_overlap(db, listing_id, check_in, check_out):
    return db.query(Booking).filter(
        Booking.listing_id == listing_id,
        Booking.status == "confirmed",
        Booking.check_in < check_out,
        Booking.check_out > check_in,
    ).first()

def create_booking(db, listing, guest_id, check_in, check_out, guests):
    if guests > listing.max_guests:
        raise HTTPException(400, "Guest count exceeds listing capacity")
    if find_overlap(db, listing.id, check_in, check_out):
        raise HTTPException(409, "Listing is unavailable for these dates")
    total = calculate_quote(listing.price_per_night, check_in, check_out)["total"]
    booking = Booking(
        listing_id=listing.id, guest_id=guest_id,
        check_in=check_in, check_out=check_out,
        guests=guests, total_price=total, status="confirmed"
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
