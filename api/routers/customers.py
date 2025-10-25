from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .. import crud, models
from ..deps import pagination_defaults

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/", response_model=List[models.CustomerOut])
def list_customers(p=Depends(pagination_defaults)):
    rows = crud.fetch_all(
        "SELECT * FROM customers ORDER BY customer_id LIMIT %s OFFSET %s",
        (p["limit"], p["skip"])
    )
    return rows

@router.get("/{customer_id}", response_model=models.CustomerOut)
def get_customer(customer_id: str):
    row = crud.fetch_one(
        "SELECT * FROM customers WHERE customer_id=%s",
        (customer_id,)
    )
    if not row:
        raise HTTPException(404, "Customer not found")
    return row

@router.post("/", status_code=201)
def create_customer(payload: models.CustomerIn):
    sql = """INSERT INTO customers
    (customer_id, name, email, phone, city, region, registration_date)
    VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    try:
        crud.execute(sql, (
            payload.customer_id, payload.name, payload.email, payload.phone,
            payload.city, payload.region, payload.registration_date
        ))
    except Exception as e:
        raise HTTPException(400, f"Insertion failed: {e}")
    return {"message": "Customer created"}

@router.put("/{customer_id}")
def update_customer(customer_id: str, payload: models.CustomerIn):
    sql = """UPDATE customers SET name=%s, email=%s, phone=%s, city=%s, region=%s, registration_date=%s
             WHERE customer_id=%s"""
    n = crud.execute(sql, (
        payload.name, payload.email, payload.phone, payload.city, payload.region,
        payload.registration_date, customer_id
    ))
    if n == 0:
        raise HTTPException(404, "Customer not found")
    return {"message": "Customer updated"}

@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: str):
    n = crud.execute("DELETE FROM customers WHERE customer_id=%s", (customer_id,))
    if n == 0:
        raise HTTPException(404, "Customer not found")
