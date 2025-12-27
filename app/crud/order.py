from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.order import Order, OrderItem, OrderStatus
from ..models.phone import Phone
from ..schemas.order import OrderCreate, OrderItemCreate
from datetime import datetime

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    user_email: Optional[str] = None,
    status: Optional[OrderStatus] = None
):
    query = db.query(Order)
    
    if user_email:
        query = query.filter(Order.user_email == user_email)
    if status:
        query = query.filter(Order.status == status)
    
    return query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

def create_order(db: Session, order: OrderCreate, user_id: Optional[int] = None):
    total_amount = 0
    order_items = []
    
    for item in order.items:
        phone = db.query(Phone).filter(Phone.id == item.phone_id).first()
        if not phone:
            raise ValueError(f"Phone with id {item.phone_id} not found")
        
        if phone.stock < item.quantity:
            raise ValueError(f"Insufficient stock for {phone.name}. Available: {phone.stock}")
        
        subtotal = phone.final_price * item.quantity
        total_amount += subtotal
        
        phone.stock -= item.quantity
        
        order_item = OrderItem(
            phone_id=item.phone_id,
            quantity=item.quantity,
            unit_price=phone.final_price,
            subtotal=subtotal
        )
        order_items.append(order_item)
    
    db_order = Order(
        user_id=user_id,
        user_email=order.user_email,
        user_name=order.user_name,
        shipping_address=order.shipping_address,
        phone_number=order.phone_number,
        total_amount=total_amount,
        items=order_items
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, status: OrderStatus):
    db_order = get_order(db, order_id)
    if db_order:
        db_order.status = status
        db_order.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order

def get_user_orders(db: Session, user_email: str, skip: int = 0, limit: int = 100):
    return db.query(Order).filter(
        Order.user_email == user_email
    ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

def calculate_cart_total(db: Session, items: List[OrderItemCreate]):
    total = 0
    cart_details = []
    
    for item in items:
        phone = db.query(Phone).filter(Phone.id == item.phone_id).first()
        if phone:
            subtotal = phone.final_price * item.quantity
            total += subtotal
            cart_details.append({
                "phone_id": phone.id,
                "name": phone.name,
                "quantity": item.quantity,
                "unit_price": phone.final_price,
                "subtotal": subtotal,
                "image_url": phone.image_url,
                "stock": phone.stock
            })
    
    return total, cart_details