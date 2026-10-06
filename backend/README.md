# Airbnb Clone Backend

## Run
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs

## Demo users
1 - Aarav Sharma - host
2 - Priya Reddy - host
3 - Shiv Guest - guest
4 - Ananya Guest - guest

Protected endpoints use the `X-User-Id` header.

## Included
- SQLite + SQLAlchemy
- Listings CRUD
- Search/filter/pagination
- Availability and overlap detection
- Server-side pricing
- Bookings/cancellation
- Favorites
- Reviews
- Host dashboard
- Seed data
- CORS
- Swagger/OpenAPI
