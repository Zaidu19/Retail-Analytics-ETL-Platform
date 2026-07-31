
from uuid import UUID
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime,timezone

from src.payments.dtos import PaymentCreateSchema,PaymentUpdateSchema
from src.common.enum import PaymentStatus
from src.payments.models import PaymentModel
from src.orders.models import OrderModel
from src.common.enum import OrderStatus


def create_payment(payload:PaymentCreateSchema,db:Session)->PaymentModel:
    order = db.get(OrderModel,payload.order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")

    if order.status == OrderStatus.cancelled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Cannot create payment for cancelled order")

    existing_payment = db.scalars(select(PaymentModel).where(PaymentModel.order_id == payload.order_id)
                                  .order_by(PaymentModel.created_at.desc())).first()
    if existing_payment:

        if existing_payment.payment_status == PaymentStatus.pending:
            return existing_payment
        
        if existing_payment.payment_status == PaymentStatus.success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Payment already completed")

        if existing_payment.payment_status == PaymentStatus.refunded:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Payment already refunded")


    new_payment = PaymentModel(
        order_id = order.id,
        amount = order.grand_total,
        payment_method = payload.payment_method,
        payment_status = PaymentStatus.pending,
        paid_at =None,
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment

def update_payment_status(payment_id:UUID,payload:PaymentUpdateSchema,db:Session)->PaymentModel:
    payment = db.get(PaymentModel,payment_id)

    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Payment not found")

    if payment.payment_status == PaymentStatus.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Payment already completed")

    if payment.payment_status == payload.payment_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Payment already has this status")

    payment.payment_status = payload.payment_status

    if payload.payment_status == PaymentStatus.success:
        order = db.get(OrderModel,payment.order_id)

        if order.status == OrderStatus.cancelled:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Cannot complete payment for cancelled order")

        order.status = OrderStatus.paid
        payment.paid_at = datetime.now(timezone.utc)

    elif payload.payment_status == PaymentStatus.failed:
        payment.paid_at = None

    elif payload.payment_status == PaymentStatus.refunded:
         pass

    db.commit()
    db.refresh(payment)    


    return payment

def get_payment_by_id(payment_id:UUID,db:Session)->PaymentModel:
    payment = db.get(PaymentModel,payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Payment not found")
    return payment

def get_list_of_payments(db:Session,skip:int=0,limit:int=100)->list[PaymentModel]:
    payments = db.scalars(select(PaymentModel).offset(skip).limit(limit)).all()
    return payments

def get_payment_by_order(order_id:UUID,db:Session)->list[PaymentModel]:
    order = db.get(OrderModel,order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    payments = db.scalars(select(PaymentModel).where(PaymentModel.order_id == order_id)).all()

    return payments



            




        
    
    