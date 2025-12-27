from sqlalchemy.orm import Session
from ..models.phone import Phone
from ..schemas.phone import PhoneCreate, PhoneUpdate
from typing import List, Optional

def get_phone(db: Session, phone_id: int):
    return db.query(Phone).filter(Phone.id == phone_id).first()

def get_phones(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    query = db.query(Phone).filter(Phone.is_active == True)
    
    if brand:
        query = query.filter(Phone.brand == brand)
    if min_price:
        query = query.filter(Phone.final_price >= min_price)
    if max_price:
        query = query.filter(Phone.final_price <= max_price)
    
    return query.offset(skip).limit(limit).all()

def create_phone(db: Session, phone: PhoneCreate):
    db_phone = Phone(**phone.dict())
    db.add(db_phone)
    db.commit()
    db.refresh(db_phone)
    return db_phone

def update_phone(db: Session, phone_id: int, phone_update: PhoneUpdate):
    db_phone = get_phone(db, phone_id)
    if db_phone:
        update_data = phone_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_phone, field, value)
        db.commit()
        db.refresh(db_phone)
    return db_phone

def delete_phone(db: Session, phone_id: int):
    db_phone = get_phone(db, phone_id)
    if db_phone:
        db.delete(db_phone)
        db.commit()
    return db_phone

def get_brands(db: Session):
    brands = db.query(Phone.brand).distinct().all()
    return [brand[0] for brand in brands]  # Extract string from tuple