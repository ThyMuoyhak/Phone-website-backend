from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItemCreate(BaseModel):
    phone_id: int
    quantity: int

class OrderItemResponse(BaseModel):
    id: int
    phone_id: int
    quantity: int
    unit_price: float
    subtotal: float
    
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    user_email: EmailStr
    user_name: str
    shipping_address: str
    phone_number: str
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderResponse(BaseModel):
    id: int
    user_email: str
    user_name: str
    shipping_address: str
    phone_number: str
    total_amount: float
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True