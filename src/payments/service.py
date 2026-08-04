
from uuid import UUID
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import select


from src.payments.dtos import PaymentUpdateSchema
from src.common.enum import PaymentStatus,UserRole
from src.users.models import UserModel
from src.payments.models import PaymentModel
from src.orders.models import OrderModel
from src.common.enum import OrderStatus
from src.payments.helper import complete_payment

VALID_PAYMENT_TRANSITIONS ={
    PaymentStatus.pending:[
        PaymentStatus.success,
        PaymentStatus.failed
    ],
    PaymentStatus.failed:[
        PaymentStatus.pending,
    ],
    PaymentStatus.success:[],
    PaymentStatus.refunded:[]
}


def update_payment_status(payment_id:UUID,payload:PaymentUpdateSchema,db:Session)->PaymentModel:
    try:
        payment = db.get(PaymentModel,payment_id)

        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Payment not found")

        if payload.payment_status == payment.payment_status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Payment already has this status.")

        if payload.payment_status not in VALID_PAYMENT_TRANSITIONS[payment.payment_status]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Cannot change payment from {payment.payment_status.value} to {payload.payment_status.value}")
        order = db.get(OrderModel,payment.order_id)
        
        if payload.payment_status == PaymentStatus.success:

            if order.status == OrderStatus.cancelled:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Cannot complete payment for cancelled order")

            complete_payment(payment,order)
        

        elif payload.payment_status == PaymentStatus.failed:
            payment.payment_status = PaymentStatus.failed
            payment.paid_at = None

        elif payload.payment_status == PaymentStatus.refunded:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Refund workflow is not implemented yet.")

        db.commit()
        db.refresh(payment)    


        return payment
    except Exception:
        db.rollback()
        raise

def get_payment_by_id(payment_id:UUID,current_user:UserModel,db:Session)->PaymentModel:
    payment = db.get(PaymentModel,payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Payment not found")
    if current_user.role == UserRole.CUSTOMER:
        if payment.order.customer.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed to access this payment")
    return payment

def get_list_of_payments(db:Session,skip:int=0,limit:int=100)->list[PaymentModel]:
    payments = db.scalars(select(PaymentModel).offset(skip).limit(limit)).all()
    return payments

def get_payment_by_order(order_id:UUID,current_user:UserModel,db:Session)->list[PaymentModel]:
    order = db.get(OrderModel,order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")

    if current_user.role == UserRole.CUSTOMER:
        if order.customer.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed to access this order's payment.")
    
    payments = db.scalars(select(PaymentModel).where(PaymentModel.order_id == order_id)).all()

    return payments



            




        
    
    