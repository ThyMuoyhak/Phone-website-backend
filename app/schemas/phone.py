from pydantic import BaseModel
from typing import Optional

class PhoneBase(BaseModel):
    name: str
    brand: str
    ram: Optional[str] = None
    storage: Optional[str] = None
    cpu: Optional[str] = None
    screen: Optional[str] = None
    battery: Optional[str] = None
    os: Optional[str] = None
    price: float
    discount: Optional[float] = 0.0
    final_price: float
    stock: Optional[int] = 0
    warranty: Optional[str] = None
    image_url: Optional[str] = None

class PhoneCreate(PhoneBase):
    pass

class PhoneUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    discount: Optional[float] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None

class Phone(PhoneBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True