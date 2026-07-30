from fastapi import HTTPException,status
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.orders.models import OrderModel
from src.customers.models import CustomerModel
from src.common.enum import OrderStatus
from src.orders.dtos import (
    OrderCreateSchema,
    OrderUpdateSchema,
)

def create_order(payload:OrderCreateSchema,db:Session)->OrderModel:
    customer =db.get(CustomerModel,payload.customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer not found")
    new_order = OrderModel(
        customer_id = payload.customer_id
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order

def get_all_orders(db:Session,skip:int=0,limit:int=50)->list[OrderModel]:
    orders =db.scalars(select(OrderModel).offset(skip).limit(limit)).all()
    return orders

def get_order_by_id(order_id:UUID,db:Session)->OrderModel:
    order = db.get(OrderModel,order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    return order

def get_orders_by_customer(customer_id:UUID,db:Session)->list[OrderModel]:
    customer = db.get(CustomerModel,customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer not found")
    orders = db.scalars(select(OrderModel).where(OrderModel.customer_id == customer_id)).all()
    return orders

def update_order(order_id:UUID,payload:OrderUpdateSchema,db:Session)->OrderModel:
    order = db.get(OrderModel,order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    
    update_data = payload.model_dump(exclude_unset=True,exclude_none=True)

    for key,value in update_data.items():
        setattr(order,key,value)

    db.commit()
    db.refresh(order)
    return order

def cancel_order(order_id:UUID,db:Session)->OrderModel:
    order = db.get(OrderModel,order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")

    if order.status == OrderStatus.cancelled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Order already cancelled")

    if order.status in (
        OrderStatus.shipped,
        OrderStatus.delivered):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Cannot cancel shipped or delivered orders")

    order.status = OrderStatus.cancelled

    db.commit()
    db.refresh(order)

    return order        



