from fastapi import HTTPException,status
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.orders.models import OrderModel
from src.customers.models import CustomerModel
from src.products.models import ProductModel
from src.orderitems.models import OrderItemModel
from src.inventory_logs.models import InventoryLogModel
from src.payments.models import PaymentModel

from src.common.enum import OrderStatus,PaymentStatus,InventoryReason
from src.common.pricing import calculate_order_total
from src.orders.dtos import (
    OrderCreateSchema,
    OrderUpdateSchema,
)

def create_order(payload:OrderCreateSchema,db:Session)->OrderModel:
    try:
        customer =db.get(CustomerModel,payload.customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Customer not found")

        stock_errors=[]
        validated_products=[]
        
        for item in payload.items:
            product = db.get(ProductModel,item.product_id)
            if not product:
                stock_errors.append({
                    "product_id":str(item.product_id),
                    "message":"Product not found"
                })
                continue

            if product.stock_qty < item.quantity:
                stock_errors.append({
                    "product_id":str(product.id),
                    "product_name":product.name,
                    "requested":item.quantity,
                    "available":product.stock_qty
                })
                continue
            validated_products.append((product,item))
        if stock_errors:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=stock_errors)    

        new_order = OrderModel(customer_id = payload.customer_id)
        db.add(new_order)
        db.flush()
                    
        pricing_items=[]    
        for product, item in validated_products:

            order_item = OrderItemModel(
                order_id = new_order.id,
                product_id = item.product_id,
                quantity = item.quantity,
                unit_price =product.price
            )
            db.add(order_item)            
            
            product.stock_qty -= item.quantity

            inventory_log = InventoryLogModel(
                product_id = item.product_id,
                change_qty = -item.quantity,
                reason = InventoryReason.sale,
            )
            db.add(inventory_log)
                
            pricing_items.append(
                (product.price,item.quantity)
            ) 
        
                       

        pricing = calculate_order_total(
                    items=pricing_items,
                )
        
        new_order.subtotal =pricing["subtotal"]
        new_order.discount = pricing["discount"]
        new_order.tax = pricing["tax"]
        new_order.grand_total = pricing["grand_total"]    

        payment = PaymentModel(
                order_id = new_order.id,
                amount = new_order.grand_total,
                payment_method = payload.payment_method,
                payment_status = PaymentStatus.pending,
                paid_at = None
            )

        db.add(payment)

        db.commit()
        db.refresh(new_order)
        db.refresh(payment)

        return new_order    
    except Exception:
        db.rollback()
        raise
 


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
    try:    
        order = db.get(OrderModel,order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
        if payload.status == OrderStatus.paid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Order is marked as PAID automatically after succesfull payment.")

        valid_transition = {
            OrderStatus.pending:[],
            OrderStatus.paid:[OrderStatus.shipped],
            OrderStatus.shipped:[OrderStatus.delivered],
            OrderStatus.delivered:[OrderStatus.completed],
            OrderStatus.completed:[],
            OrderStatus.cancelled:[],
        }

        if payload.status not in valid_transition[order.status]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Cannot change order from {order.status.value} to {payload.status.value}")
        
        order.status = payload.status

        db.commit()
        db.refresh(order)
        return order
    except Exception:
        db.rollback()
        raise




def cancel_order(order_id:UUID,db:Session)->OrderModel:
    try:    
        order = db.get(OrderModel,order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")

        if order.status == OrderStatus.cancelled:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Order already cancelled")

        if order.status in (
            OrderStatus.shipped,
            OrderStatus.delivered):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Cannot cancel shipped or delivered orders")

        payment = db.scalars(select(PaymentModel)
                             .where(PaymentModel.order_id == order.id)
                             .order_by(PaymentModel.created_at.desc())).first()

        if payment and payment.payment_status == PaymentStatus.success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Paid orders must be refunded before cancellation")

        for item in order.order_items:
            product = db.get(ProductModel,item.product_id)

            product.stock_qty += item.quantity

            inventory_log = InventoryLogModel(
                product_id = product.id,
                change_qty = item.quantity,
                reason = InventoryReason.return_
            )
            db.add(inventory_log)

        order.status = OrderStatus.cancelled

        db.commit()
        db.refresh(order)

        return order 
    
    except Exception:
        db.rollback()
    raise           



