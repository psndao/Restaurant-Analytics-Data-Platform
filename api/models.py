from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

# --- Customers ---
class CustomerIn(BaseModel):
    customer_id: str = Field(..., max_length=10)
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    registration_date: Optional[date] = None

class CustomerOut(CustomerIn):
    pass

# --- Staff ---
class StaffIn(BaseModel):
    staff_id: str = Field(..., max_length=10)
    name: Optional[str] = None
    role: Optional[str] = None
    hire_date: Optional[date] = None
    salary: Optional[float] = None

class StaffOut(StaffIn):
    pass

# --- Menu ---
class MenuIn(BaseModel):
    menu_id: str = Field(..., max_length=10)
    dish_name: Optional[str] = None
    price: Optional[float] = None

class MenuOut(MenuIn):
    pass

# --- Orders ---
class OrderIn(BaseModel):
    order_id: str = Field(..., max_length=10)
    customer_id: Optional[str] = None
    menu_id: Optional[str] = None
    staff_id: Optional[str] = None
    order_date: Optional[date] = None
    quantity: Optional[int] = None
    total_amount: Optional[float] = None

class OrderOut(OrderIn):
    pass

# --- Deliveries ---
class DeliveryIn(BaseModel):
    delivery_id: str = Field(..., max_length=10)
    order_id: Optional[str] = None
    delivery_person: Optional[str] = None
    delivery_time: Optional[datetime] = None
    status: Optional[str] = None

class DeliveryOut(DeliveryIn):
    pass

# --- Bookings ---
class BookingIn(BaseModel):
    booking_id: str = Field(..., max_length=10)
    customer_id: Optional[str] = None
    staff_id: Optional[str] = None
    booking_date: Optional[date] = None
    num_people: Optional[int] = None
    status: Optional[str] = None

class BookingOut(BookingIn):
    pass
