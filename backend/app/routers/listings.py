from datetime import date
from math import ceil
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query
from app.database import get_db
from app.models import Listing, ListingImage, ListingAmenity, Amenity, Booking, Review, Favorite
from app.schemas import ListingCreate, ListingUpdate, ListingCard, ListingDetail, PageListings, QuoteOut
from app.dependencies.auth import require_host
from app.services.pricing import calculate_quote

router = APIRouter(prefix="/listings", tags=["Listings"])

def make_card(db, listing):
    avg = db.query(func.avg(Review.rating)).filter(Review.listing_id == listing.id).scalar()
    count = db.query(func.count(Review.id)).filter(Review.listing_id == listing.id).scalar() or 0
    image = db.query(ListingImage).filter(
        ListingImage.listing_id == listing.id
    ).order_by(ListingImage.is_primary.desc()).first()
    return ListingCard(
        id=listing.id, title=listing.title, location=listing.location,
        price_per_night=listing.price_per_night, property_type=listing.property_type,
        max_guests=listing.max_guests, primary_image=image.image_url if image else None,
        rating=round(float(avg or 0), 1), review_count=count
    )

@router.get("", response_model=PageListings)
def list_listings(
    location: str | None = None,
    check_in: date | None = None,
    check_out: date | None = None,
    guests: int | None = Query(None, ge=1),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    property_type: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db)
):
    q = db.query(Listing)
    if location:
        q = q.filter(Listing.location.ilike(f"%{location}%"))
    if guests:
        q = q.filter(Listing.max_guests >= guests)
    if min_price is not None:
        q = q.filter(Listing.price_per_night >= min_price)
    if max_price is not None:
        q = q.filter(Listing.price_per_night <= max_price)
    if property_type:
        q = q.filter(Listing.property_type.ilike(property_type))
    if check_in and check_out:
        if check_out <= check_in:
            raise HTTPException(400, "check_out must be after check_in")
        q = q.filter(~Listing.bookings.any(
            (Booking.status == "confirmed") &
            (Booking.check_in < check_out) &
            (Booking.check_out > check_in)
        ))
    total = q.count()
    rows = q.order_by(Listing.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return PageListings(
        items=[make_card(db, x) for x in rows],
        page=page, page_size=page_size, total=total,
        pages=ceil(total / page_size) if total else 0
    )

@router.get("/{listing_id}", response_model=ListingDetail)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(404, "Listing not found")
    card = make_card(db, listing)
    images = db.query(ListingImage).filter(ListingImage.listing_id == listing_id).all()
    amenities = [
        x.amenity.name for x in db.query(ListingAmenity)
        .filter(ListingAmenity.listing_id == listing_id).all()
    ]
    return ListingDetail(
        **card.model_dump(), description=listing.description,
        host=listing.host, images=images, amenities=amenities
    )

@router.post("", response_model=ListingDetail, status_code=201)
def create_listing(payload: ListingCreate, db: Session = Depends(get_db), host=Depends(require_host)):
    listing = Listing(
        host_id=host.id, title=payload.title, description=payload.description,
        location=payload.location, price_per_night=payload.price_per_night,
        property_type=payload.property_type, max_guests=payload.max_guests
    )
    db.add(listing)
    db.flush()
    for image in payload.images:
        db.add(ListingImage(listing_id=listing.id, **image.model_dump()))
    for name in set(payload.amenities):
        amenity = db.query(Amenity).filter(Amenity.name == name).first()
        if not amenity:
            amenity = Amenity(name=name)
            db.add(amenity)
            db.flush()
        db.add(ListingAmenity(listing_id=listing.id, amenity_id=amenity.id))
    db.commit()
    db.refresh(listing)
    return get_listing(listing.id, db)

@router.patch("/{listing_id}", response_model=ListingDetail)
def update_listing(listing_id: int, payload: ListingUpdate, db: Session = Depends(get_db), host=Depends(require_host)):
    listing = db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(404, "Listing not found")
    if listing.host_id != host.id:
        raise HTTPException(403, "You do not own this listing")
    data = payload.model_dump(exclude_unset=True)
    images = data.pop("images", None)
    amenities = data.pop("amenities", None)
    for key, value in data.items():
        setattr(listing, key, value)
    if images is not None:
        db.query(ListingImage).filter(ListingImage.listing_id == listing_id).delete()
        for image in images:
            db.add(ListingImage(listing_id=listing_id, **image.model_dump()))
    if amenities is not None:
        db.query(ListingAmenity).filter(ListingAmenity.listing_id == listing_id).delete()
        for name in set(amenities):
            amenity = db.query(Amenity).filter(Amenity.name == name).first()
            if not amenity:
                amenity = Amenity(name=name)
                db.add(amenity)
                db.flush()
            db.add(ListingAmenity(listing_id=listing_id, amenity_id=amenity.id))
    db.commit()
    return get_listing(listing_id, db)

@router.delete("/{listing_id}", status_code=204)
def delete_listing(listing_id: int, db: Session = Depends(get_db), host=Depends(require_host)):
    listing = db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(404, "Listing not found")
    if listing.host_id != host.id:
        raise HTTPException(403, "You do not own this listing")
    upcoming = db.query(Booking).filter(
        Booking.listing_id == listing_id,
        Booking.status == "confirmed",
        Booking.check_out >= date.today()
    ).first()
    if upcoming:
        raise HTTPException(409, "Cannot delete listing with upcoming confirmed bookings")
    db.delete(listing)
    db.commit()

@router.get("/{listing_id}/unavailable-dates")
def unavailable_dates(listing_id: int, db: Session = Depends(get_db)):
    if not db.get(Listing, listing_id):
        raise HTTPException(404, "Listing not found")
    rows = db.query(Booking).filter(
        Booking.listing_id == listing_id, Booking.status == "confirmed"
    ).all()
    return [{"check_in": b.check_in, "check_out": b.check_out} for b in rows]

@router.get("/{listing_id}/quote", response_model=QuoteOut)
def quote(listing_id: int, check_in: date, check_out: date, db: Session = Depends(get_db)):
    listing = db.get(Listing, listing_id)
    if not listing:
        raise HTTPException(404, "Listing not found")
    if check_out <= check_in:
        raise HTTPException(400, "check_out must be after check_in")
    overlap = db.query(Booking).filter(
        Booking.listing_id == listing_id, Booking.status == "confirmed",
        Booking.check_in < check_out, Booking.check_out > check_in
    ).first()
    if overlap:
        raise HTTPException(409, "Listing unavailable for these dates")
    return calculate_quote(listing.price_per_night, check_in, check_out)
