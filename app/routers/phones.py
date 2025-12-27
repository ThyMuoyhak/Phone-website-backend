from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.phone import Phone, PhoneCreate, PhoneUpdate
from ..crud import phone as crud_phone

router = APIRouter(prefix="/api/phones", tags=["phones"])

@router.get("/", response_model=List[Phone])
def read_phones(
    skip: int = 0,
    limit: int = 100,
    brand: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    phones = crud_phone.get_phones(
        db, skip=skip, limit=limit, 
        brand=brand, min_price=min_price, max_price=max_price
    )
    return phones

@router.get("/{phone_id}", response_model=Phone)
def read_phone(phone_id: int, db: Session = Depends(get_db)):
    db_phone = crud_phone.get_phone(db, phone_id=phone_id)
    if db_phone is None:
        raise HTTPException(status_code=404, detail="Phone not found")
    return db_phone

@router.post("/", response_model=Phone)
def create_phone(phone: PhoneCreate, db: Session = Depends(get_db)):
    return crud_phone.create_phone(db=db, phone=phone)

@router.put("/{phone_id}", response_model=Phone)
def update_phone(phone_id: int, phone: PhoneUpdate, db: Session = Depends(get_db)):
    return crud_phone.update_phone(db=db, phone_id=phone_id, phone_update=phone)

@router.delete("/{phone_id}")
def delete_phone(phone_id: int, db: Session = Depends(get_db)):
    crud_phone.delete_phone(db=db, phone_id=phone_id)
    return {"message": "Phone deleted successfully"}

@router.get("/brands/list")
def get_brands(db: Session = Depends(get_db)):
    return crud_phone.get_brands(db)