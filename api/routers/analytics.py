from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from .. import crud
from ..deps import pagination_defaults

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/sales-by-menu")
def sales_by_menu(p=Depends(pagination_defaults)) -> List[Dict[str, Any]]:
    # utilise la vue v_sales_by_menu si créée, sinon calcule à la volée
    rows = crud.fetch_all(
        "SELECT dish_name, total_quantity, total_revenue FROM v_sales_by_menu LIMIT %s OFFSET %s",
        (p["limit"], p["skip"])
    )
    return rows

@router.get("/staff-performance")
def staff_performance(p=Depends(pagination_defaults)) -> List[Dict[str, Any]]:
    rows = crud.fetch_all(
        "SELECT staff_name, role, total_orders, total_sales FROM v_staff_performance LIMIT %s OFFSET %s",
        (p["limit"], p["skip"])
    )
    return rows

@router.get("/delivery-status")
def delivery_status() -> List[Dict[str, Any]]:
    rows = crud.fetch_all("SELECT status, total_deliveries, pct FROM v_delivery_status")
    return rows

@router.get("/bookings-monthly")
def bookings_monthly(p=Depends(pagination_defaults)) -> List[Dict[str, Any]]:
    rows = crud.fetch_all(
        "SELECT month, total_bookings, total_guests FROM v_bookings_monthly LIMIT %s OFFSET %s",
        (p["limit"], p["skip"])
    )
    return rows
