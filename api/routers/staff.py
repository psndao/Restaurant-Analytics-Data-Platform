from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .. import crud, models
from ..deps import pagination_defaults

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.get("/", response_model=List[models.StaffOut])
def list_staff(p=Depends(pagination_defaults)):
    rows = crud.fetch_all(
        "SELECT * FROM staff ORDER BY staff_id LIMIT %s OFFSET %s",
        (p["limit"], p["skip"])
    )
    return rows

@router.post("/", status_code=201)
def create_staff(payload: models.StaffIn):
    sql = """INSERT INTO staff (staff_id, name, role, hire_date, salary)
             VALUES (%s,%s,%s,%s,%s)"""
    try:
        crud.execute(sql, (payload.staff_id, payload.name, payload.role, payload.hire_date, payload.salary))
    except Exception as e:
        raise HTTPException(400, f"Insertion failed: {e}")
    return {"message": "Staff created"}
