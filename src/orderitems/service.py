
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from sqlalchemy import select
from uuid import UUID

from src.common.enum import OrderStatus
from src.orders.models import OrderModel
from src.products.models import ProductModel
from src.orderitems.models import OrderItemModel
from src.orderitems.dtos import(
    OrderItemCreateSchema,
    OrderItemUpdateSchema
)

def create_orderitem(payload:OrderItemCreateSchema,db:Session)->OrderItemModel:
    order = db.get(OrderModel,payload.order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    if order.status in(
        OrderStatus.shipped,
        OrderStatus.delivered,
        OrderStatus.completed,
        OrderStatus.cancelled,
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Cannot add items to processed order")
    
    product = db.get(ProductModel,payload.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    
    if product.stock_qty < payload.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Insufficient stock")
    
    order_item = db.scalars(select(OrderItemModel).where(
        OrderItemModel.order_id == payload.order_id,
        OrderItemModel.product_id == payload.product_id,
    )).first()

    if order_item:
        order_item.quantity += payload.quantity

    else:
        order_item = OrderItemModel(
            order_id = payload.order_id,
            product_id = payload.product_id,
            quantity = payload.quantity,
            unit_price = product.price
        )    
        db.add(order_item)
        db.flush()

    product.stock_qty -= payload.quantity

    subtotal = sum(
        item.quantity * item.unit_price
        for item in order.order_items
    )    

    order.subtotal = subtotal

    db.commit()
    db.refresh(order_item)

    return order_item


def get_order_item_by_id(order_item_id:UUID,db:Session)->OrderItemModel:
    order_item = db.get(OrderItemModel,order_item_id)
    if not order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order Item not found")
    return order_item

def get_list_order_items(db:Session,skip:int=0,limit:int=100)->list[OrderItemModel]:
    order_items = db.scalars(select(OrderItemModel).offset(skip).limit(limit)).all()
    return order_items

def get_order_items_by_order(order_id:UUID,db:Session)->list[OrderItemModel]:
    order = db.get(OrderModel,order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    order_items = db.scalars(select(OrderItemModel).where(OrderItemModel.order_id == order_id)).all()

    return order_items

def update_order_items(order_item_id:UUID,payload:OrderItemUpdateSchema,db:Session)->OrderItemModel:
    order_item = db.get(OrderItemModel,order_item_id)
    if not order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order Item not found")
    
    product = db.get(ProductModel,order_item.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")

    order = db.get(OrderModel,order_item.order_id)

    if order.status in(
        OrderStatus.shipped,
        OrderStatus.delivered,
        OrderStatus.completed,
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Cannot modify a processed order")

    old_quantity =order_item.quantity
    new_quantity = payload.quantity

    difference = new_quantity - old_quantity

    if difference > 0:
        if product.stock_qty < difference:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Insufficient stock")

        product.stock_qty -= difference
    elif difference < 0:
        product.stock_qty += abs(difference)

    order_item.quantity = new_quantity   

    subtotal = sum(
        item.quantity * item.unit_price
        for item in order.order_items
    )      

    order.subtotal = subtotal

    db.commit()
    db.refresh(order_item)

    return order_item

def delete_order_item(order_item_id:UUID,db:Session):
    order_item = db.get(OrderItemModel,order_item_id)
    if not order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order Item not found")

    product = db.get(ProductModel,order_item.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    
    order = db.get(OrderModel,order_item.order_id)

    if order.status in(
        OrderStatus.shipped,
        OrderStatus.delivered,
        OrderStatus.completed,
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Cannot delete items from processed orders")

    product.stock_qty += order_item.quantity

    db.delete(order_item)
    db.flush()

    subtotal = sum(
        item.quantity * item.unit_price
        for item in order.order_items
    )

    order.subtotal = subtotal

    db.commit()
    return



    

        



