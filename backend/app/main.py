from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.config import CORS_ORIGINS, SEED_ON_STARTUP
from app.seed.seed import seed
from app.routers import users, amenities, listings, bookings, favorites, reviews, host

app = FastAPI(title="Airbnb Clone API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
for router in [users.router, amenities.router, listings.router, bookings.router, favorites.router, reviews.router, host.router]:
    app.include_router(router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    if SEED_ON_STARTUP:
        seed()

@app.get("/")
def root():
    return {"message": "Airbnb Clone API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
