from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Listing, Booking
from app.schemas import HostStats
from app.dependencies.auth import require_host

router = APIRouter(prefix="/host", tags=["Host"])

@router.get("/listings")
def host_listings(db: Session = Depends(get_db), host=Depends(require_host)):
    return db.query(Listing).filter(Listing.host_id == host.id).order_by(Listing.created_at.desc()).all()

@router.get("/bookings")
def host_bookings(db: Session = Depends(get_db), host=Depends(require_host)):
    return db.query(Booking).join(Listing).filter(Listing.host_id == host.id).order_by(Booking.check_in.desc()).all()

@router.get("/stats", response_model=HostStats)
def host_stats(db: Session = Depends(get_db), host=Depends(require_host)):
    listings = db.query(Listing).filter(Listing.host_id == host.id).all()
    ids = [x.id for x in listings]
    bookings = db.query(Booking).filter(Booking.listing_id.in_(ids)).all() if ids else []
    confirmed = [b for b in bookings if b.status == "confirmed"]
    return HostStats(
        listing_count=len(listings),
        booking_count=len(bookings),
        confirmed_booking_count=len(confirmed),
        revenue=round(sum(b.total_price for b in confirmed), 2)
    )
