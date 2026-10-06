# Stayly — Airbnb-style Full Stack Frontend

Next.js 15 + TypeScript frontend for the supplied FastAPI Airbnb assignment backend.

## Run

```bash
npm install
```

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
NEXT_PUBLIC_USER_ID=3
```

Then:

```bash
npm run dev
```

Open http://localhost:3000

## Mock users

- Aarav (id 1) — host
- Priya (id 2) — host
- Shiv (id 3) — guest
- Ananya (id 4) — guest

The user selector in the navbar switches the mock identity. Host pages are protected by `HostGuard`.

## Backend

Start the supplied FastAPI backend on port 8000. The frontend sends `X-User-Id` with every API request.

## Main routes

- `/` Explore/search
- `/listings/:id` Listing details
- `/book/:listingId` Booking
- `/trips` Guest trips
- `/trips/:id` Trip details/cancel
- `/wishlist` Wishlist
- `/host` Host dashboard
- `/host/listings` Host CRUD list
- `/host/listings/new` Create listing
- `/host/listings/:id/edit` Edit listing
- `/host/bookings` Host bookings
