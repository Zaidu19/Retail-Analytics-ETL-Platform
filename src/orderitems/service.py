
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from sqlalchemy import select
from uuid import UUID


from src.orders.models import OrderModel
from src.orderitems.models import OrderItemModel
from src.users.models import UserModel
from src.common.enum import UserRole




def get_order_item_by_id(order_item_id:UUID,current_user:UserModel,db:Session)->OrderItemModel:
    order_item = db.get(OrderItemModel,order_item_id)
    if not order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order Item not found")
    if current_user.role == UserRole.CUSTOMER:
        if order_item.order.customer.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed to access this")
    return order_item

def get_list_order_items(db:Session,skip:int=0,limit:int=100)->list[OrderItemModel]:
    order_items = db.scalars(select(OrderItemModel).offset(skip).limit(limit)).all()
    return order_items

def get_order_items_by_order(order_id:UUID,current_user:UserModel,db:Session)->list[OrderItemModel]:
    order = db.get(OrderModel,order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    if current_user.role == UserRole.CUSTOMER:
        if order.customer.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed to access this.")
    
    order_items = db.scalars(select(OrderItemModel).where(OrderItemModel.order_id == order_id)).all()

    return order_items

