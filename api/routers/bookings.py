from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .. import crud, models
from ..deps import pagination_defaults

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.get("/", response_model=List[models.BookingOut])
def list_bookings(p=Depends(pagination_defaults)):
    rows = crud.fetch_all(
        "SELECT * FROM bookings ORDER BY booking_date DESC LIMIT %s OFFSET %s",
        (p["limit"], p["skip"])
    )
    return rows

@router.post("/", status_code=201)
def create_booking(payload: models.BookingIn):
    sql = """INSERT INTO bookings
    (booking_id, customer_id, staff_id, booking_date, num_people, status)
    VALUES (%s,%s,%s,%s,%s,%s)"""
    try:
        crud.execute(sql, (
            payload.booking_id, payload.customer_id, payload.staff_id,
            payload.booking_date, payload.num_people, payload.status
        ))
    except Exception as e:
        raise HTTPException(400, f"Insertion failed: {e}")
    return {"message": "Booking created"}
