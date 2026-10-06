from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict, model_validator

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    role: str

class ImageCreate(BaseModel):
    image_url: str
    is_primary: bool = False

class ImageOut(ImageCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ListingCreate(BaseModel):
    title: str
    description: str
    location: str
    price_per_night: float = Field(gt=0)
    property_type: str
    max_guests: int = Field(gt=0)
    images: list[ImageCreate] = []
    amenities: list[str] = []

class ListingUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    price_per_night: float | None = Field(default=None, gt=0)
    property_type: str | None = None
    max_guests: int | None = Field(default=None, gt=0)
    images: list[ImageCreate] | None = None
    amenities: list[str] | None = None

class ListingCard(BaseModel):
    id: int
    title: str
    location: str
    price_per_night: float
    property_type: str
    max_guests: int
    primary_image: str | None
    rating: float
    review_count: int
    is_favorite: bool = False

class ListingDetail(ListingCard):
    description: str
    host: UserOut
    images: list[ImageOut]
    amenities: list[str]

class PageListings(BaseModel):
    items: list[ListingCard]
    page: int
    page_size: int
    total: int
    pages: int

class QuoteOut(BaseModel):
    nights: int
    nightly_total: float
    cleaning_fee: float
    service_fee: float
    total: float

class BookingCreate(BaseModel):
    listing_id: int
    check_in: date
    check_out: date
    guests: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out <= self.check_in:
            raise ValueError("check_out must be after check_in")
        return self

class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    listing_id: int
    guest_id: int
    check_in: date
    check_out: date
    guests: int
    total_price: float
    status: str
    created_at: datetime

class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = None

class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    listing_id: int
    user_id: int
    rating: int
    comment: str | None
    created_at: datetime

class HostStats(BaseModel):
    listing_count: int
    booking_count: int
    confirmed_booking_count: int
    revenue: float
