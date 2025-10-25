from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .. import crud, models
from ..deps import pagination_defaults

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=List[models.OrderOut])
def list_orders(p=Depends(pagination_defaults)):
    rows = crud.fetch_all(
        "SELECT * FROM orders ORDER BY order_date DESC, order_id LIMIT %s OFFSET %s",
        (p["limit"], p["skip"])
    )
    return rows

@router.post("/", status_code=201)
def create_order(payload: models.OrderIn):
    # La FK sera vérifiée par MySQL (customer_id, menu_id, staff_id)
    sql = """INSERT INTO orders
    (order_id, customer_id, menu_id, staff_id, order_date, quantity, total_amount)
    VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    try:
        crud.execute(sql, (
            payload.order_id, payload.customer_id, payload.menu_id,
            payload.staff_id, payload.order_date, payload.quantity, payload.total_amount
        ))
    except Exception as e:
        raise HTTPException(400, f"Insertion failed: {e}")
    return {"message": "Order created"}
