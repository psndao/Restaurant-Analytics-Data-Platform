from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .. import crud, models
from ..deps import pagination_defaults

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.get("/", response_model=List[models.MenuOut])
def list_menu(p=Depends(pagination_defaults)):
    rows = crud.fetch_all(
        "SELECT * FROM menu ORDER BY menu_id LIMIT %s OFFSET %s",
        (p["limit"], p["skip"])
    )
    return rows

@router.post("/", status_code=201)
def create_menu(payload: models.MenuIn):
    sql = "INSERT INTO menu (menu_id, dish_name, price) VALUES (%s,%s,%s)"
    try:
        crud.execute(sql, (payload.menu_id, payload.dish_name, payload.price))
    except Exception as e:
        raise HTTPException(400, f"Insertion failed: {e}")
    return {"message": "Menu item created"}
