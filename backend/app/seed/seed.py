from datetime import date, timedelta
from app.database import Base, engine, SessionLocal
from app.models import User, Listing, ListingImage, Amenity, ListingAmenity, Booking, Review

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).count():
            return
        users = [
            User(name="Aarav Sharma", email="aarav@example.com", role="host"),
            User(name="Priya Reddy", email="priya@example.com", role="host"),
            User(name="Shiv Guest", email="guest@example.com", role="guest"),
            User(name="Ananya Guest", email="ananya@example.com", role="guest"),
        ]
        db.add_all(users)
        db.flush()

        amenity_names = ["WiFi", "Pool", "Kitchen", "Air conditioning", "Parking", "Workspace", "TV", "Washer"]
        amenity_map = {}
        for name in amenity_names:
            a = Amenity(name=name)
            db.add(a)
            db.flush()
            amenity_map[name] = a

        data = [
            ("Beachfront Villa in Goa", "A peaceful villa near the beach with a private pool.", "Goa, India", 8500, "Villa", 6, ["WiFi","Pool","Kitchen","Air conditioning","Parking"], "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1200"),
            ("Modern Apartment in Hyderabad", "Stylish city apartment close to restaurants and offices.", "Hyderabad, India", 4200, "Apartment", 4, ["WiFi","Kitchen","Air conditioning","Workspace","TV"], "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=1200"),
            ("Mountain Cabin in Manali", "Cozy cabin with beautiful mountain views.", "Manali, India", 6000, "Cabin", 5, ["WiFi","Kitchen","Parking","TV"], "https://images.unsplash.com/photo-1510798831971-661eb04b3739?w=1200"),
            ("Luxury Home in Jaipur", "Traditional-modern home in the heart of Jaipur.", "Jaipur, India", 7500, "House", 8, ["WiFi","Pool","Kitchen","Air conditioning","Parking"], "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=1200"),
            ("City Studio in Bangalore", "Compact studio perfect for work or a short city stay.", "Bangalore, India", 3200, "Studio", 2, ["WiFi","Workspace","Air conditioning","Washer"], "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=1200"),
            ("Backwater Retreat in Kerala", "Relaxing stay surrounded by Kerala greenery and waterways.", "Alappuzha, Kerala", 6800, "Villa", 6, ["WiFi","Pool","Kitchen","Parking","TV"], "https://images.unsplash.com/photo-1601918774946-25832a4be0d6?w=1200"),
        ]

        listings = []
        for i, row in enumerate(data):
            title, description, location, price, property_type, max_guests, amenities, image = row
            listing = Listing(
                host_id=users[i % 2].id, title=title, description=description,
                location=location, price_per_night=price,
                property_type=property_type, max_guests=max_guests
            )
            db.add(listing)
            db.flush()
            listings.append(listing)
            db.add(ListingImage(listing_id=listing.id, image_url=image, is_primary=True))
            for name in amenities:
                db.add(
    ListingAmenity(
        listing_id=listing.id,
        amenity_id=amenity_map[name].id
    )
)

        booking = Booking(
            listing_id=listings[0].id, guest_id=users[2].id,
            check_in=date.today() + timedelta(days=20),
            check_out=date.today() + timedelta(days=23),
            guests=2, total_price=0, status="confirmed"
        )
        db.add(booking)
        db.flush()
        booking.total_price = round(8500 * 3 + 40 + (8500 * 3 * 0.12), 2)

        db.add(Review(listing_id=listings[0].id, user_id=users[2].id, rating=5, comment="Amazing stay!"))
        db.add(Review(listing_id=listings[1].id, user_id=users[3].id, rating=4, comment="Clean and comfortable."))
        db.commit()
    finally:
        db.close()
