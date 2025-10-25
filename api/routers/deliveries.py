from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .. import crud, models
from ..deps import pagination_defaults

router = APIRouter(prefix="/deliveries", tags=["Deliveries"])

@router.get("/", response_model=List[models.DeliveryOut])
def list_deliveries(p=Depends(pagination_defaults)):
    rows = crud.fetch_all(
        "SELECT * FROM deliveries ORDER BY delivery_time DESC LIMIT %s OFFSET %s",
        (p["limit"], p["skip"])
    )
    return rows

@router.post("/", status_code=201)
def create_delivery(payload: models.DeliveryIn):
    sql = """INSERT INTO deliveries
    (delivery_id, order_id, delivery_person, delivery_time, status)
    VALUES (%s,%s,%s,%s,%s)"""
    try:
        crud.execute(sql, (
            payload.delivery_id, payload.order_id, payload.delivery_person,
            payload.delivery_time, payload.status
        ))
    except Exception as e:
        raise HTTPException(400, f"Insertion failed: {e}")
    return {"message": "Delivery created"}
