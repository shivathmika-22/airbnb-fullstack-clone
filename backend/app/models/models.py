from datetime import datetime, date
from sqlalchemy import String, Integer, Float, Boolean, Date, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    listings = relationship("Listing", back_populates="host")
    bookings = relationship("Booking", back_populates="guest")
    reviews = relationship("Review", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")

class Listing(Base):
    __tablename__ = "listings"
    __table_args__ = (
        CheckConstraint("price_per_night > 0"),
        CheckConstraint("max_guests > 0"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    host_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False, index=True)
    price_per_night: Mapped[float] = mapped_column(Float, nullable=False)
    property_type: Mapped[str] = mapped_column(String, nullable=False)
    max_guests: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    host = relationship("User", back_populates="listings")
    images = relationship("ListingImage", back_populates="listing", cascade="all, delete-orphan")
    listing_amenities = relationship("ListingAmenity", back_populates="listing", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="listing")
    reviews = relationship("Review", back_populates="listing", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="listing", cascade="all, delete-orphan")

class ListingImage(Base):
    __tablename__ = "listing_images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    listing = relationship("Listing", back_populates="images")

class Amenity(Base):
    __tablename__ = "amenities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    listing_amenities = relationship("ListingAmenity", back_populates="amenity")

class ListingAmenity(Base):
    __tablename__ = "listing_amenities"
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id", ondelete="CASCADE"), primary_key=True)
    amenity_id: Mapped[int] = mapped_column(ForeignKey("amenities.id"), primary_key=True)
    listing = relationship("Listing", back_populates="listing_amenities")
    amenity = relationship("Amenity", back_populates="listing_amenities")

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("check_out > check_in"),
        CheckConstraint("guests > 0"),
        CheckConstraint("total_price >= 0"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, index=True)
    guest_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    check_in: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    check_out: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    guests: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="confirmed")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    listing = relationship("Listing", back_populates="bookings")
    guest = relationship("User", back_populates="bookings")

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (CheckConstraint("rating BETWEEN 1 AND 5"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    listing = relationship("Listing", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

class Favorite(Base):
    __tablename__ = "favorites"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id", ondelete="CASCADE"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="favorites")
    listing = relationship("Listing", back_populates="favorites")
