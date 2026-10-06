from app.config import CLEANING_FEE, SERVICE_FEE_RATE

def calculate_quote(price_per_night, check_in, check_out):
    nights = (check_out - check_in).days
    if nights <= 0:
        raise ValueError("Invalid date range")
    nightly_total = round(price_per_night * nights, 2)
    cleaning_fee = round(CLEANING_FEE, 2)
    service_fee = round(nightly_total * SERVICE_FEE_RATE, 2)
    return {
        "nights": nights,
        "nightly_total": nightly_total,
        "cleaning_fee": cleaning_fee,
        "service_fee": service_fee,
        "total": round(nightly_total + cleaning_fee + service_fee, 2),
    }
