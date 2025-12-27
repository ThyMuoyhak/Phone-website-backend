from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.order import OrderCreate, OrderResponse, OrderUpdate, OrderStatus
from ..crud import order as crud_order
from ..auth.security import get_current_active_user, User

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    try:
        user_id = current_user.username if current_user else None
        return crud_order.create_order(db=db, order=order, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[OrderResponse])
async def read_orders(
    skip: int = 0,
    limit: int = 100,
    user_email: Optional[str] = Query(None),
    status: Optional[OrderStatus] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not current_user.is_admin:
        user_email = current_user.email
    
    orders = crud_order.get_orders(
        db, skip=skip, limit=limit, 
        user_email=user_email, status=status
    )
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
async def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_order = crud_order.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if not current_user.is_admin and db_order.user_email != current_user.email:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    
    return db_order

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can update orders")
    
    db_order = crud_order.update_order_status(
        db=db, order_id=order_id, status=order_update.status
    )
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return db_order

@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete orders")
    
    crud_order.delete_order(db=db, order_id=order_id)
    return {"message": "Order deleted successfully"}

@router.post("/cart/calculate")
async def calculate_cart(
    items: List[dict],
    db: Session = Depends(get_db)
):
    try:
        order_items = []
        for item in items:
            order_items.append({"phone_id": item["phone_id"], "quantity": item["quantity"]})
        
        total, details = crud_order.calculate_cart_total(db, order_items)
        return {
            "total": total,
            "details": details,
            "item_count": len(items)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))