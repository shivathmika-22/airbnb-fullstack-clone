import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./airbnb.db")
CORS_ORIGINS = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if x.strip()]
SEED_ON_STARTUP = os.getenv("SEED_ON_STARTUP", "true").lower() == "true"
CLEANING_FEE = float(os.getenv("CLEANING_FEE", "40"))
SERVICE_FEE_RATE = float(os.getenv("SERVICE_FEE_RATE", "0.12"))
