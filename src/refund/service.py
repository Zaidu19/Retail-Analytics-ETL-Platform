
from fastapi import HTTPException,status
from uuid import UUID
from datetime import datetime,timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.refund.dtos import RefundCreateSchema
from src.inventory_logs.models import InventoryLogModel
from src.refund.models import RefundModel
from src.users.models import UserModel
from src.orders.models import OrderModel
from src.common.enum import OrderStatus,PaymentStatus,RefundStatus,InventoryReason,UserRole




def create_refund(payload:RefundCreateSchema,current_user:UserModel,db:Session)->RefundModel:
    try:
        order = db.get(OrderModel,payload.order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found.")
        
        if order.customer.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed to request a refund for this order.")
        if order.status != OrderStatus.completed:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Only completed orders can be refunded.")  

        payment = order.payment

        if payment.payment_status != PaymentStatus.success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Only succesfull payment will refunded.")

        existing_refund = db.scalars(select(RefundModel).where(RefundModel.order_id == order.id)).first()

        if existing_refund:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Refund request already exists.")

        refund = RefundModel(
            order_id=order.id,
            amount = order.grand_total,
            reason = payload.reason,
            status = RefundStatus.pending
        )

        db.add(refund)
        db.commit()
        db.refresh(refund)

        return refund
    except Exception:
        db.rollback()
        raise

def approve_refund(refund_id:UUID,db:Session)->RefundModel:
    try:
        refund =db.get(RefundModel,refund_id)

        if not refund:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Refund not found.")
        
        if refund.status == RefundStatus.approved:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Refund has already been approved.")

        if refund.status == RefundStatus.rejected:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Rejected refund cannot be approved.")

        order = refund.order
        payment = order.payment

        if payment.payment_status == PaymentStatus.refunded:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Payment already has been refunded.")
        if payment.payment_status != PaymentStatus.success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Only successful payments can be refunded.")

        refund.status = RefundStatus.approved
        refund.processed_at = datetime.now(timezone.utc)

        payment.payment_status = PaymentStatus.refunded
        order.status = OrderStatus.refunded



        for item in order.order_items:
            product = item.product

            product.stock_qty += item.quantity

            inventory = InventoryLogModel(
                product_id=item.product_id,
                change_qty=item.quantity,
                reason=InventoryReason.return_
            )  
            db.add(inventory)
            db.flush()

        db.commit()
        db.refresh(refund)

        return refund
    except Exception:
        db.rollback()
        raise

def reject_refund(refund_id:UUID,db:Session)->RefundModel:
    try:
        refund = db.get(RefundModel,refund_id)

        if not refund:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Refund not found.")

        if refund.status == RefundStatus.approved:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Approved refund cannot be rejected.")

        if refund.status == RefundStatus.rejected:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Refund has already been rejected.")

        refund.status = RefundStatus.rejected
        refund.processed_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(refund)

        return refund
    except Exception:
        db.rollback()
        raise

def get_refund_by_id(refund_id:UUID,current_user:UserModel,db:Session)->RefundModel:
    refund = db.get(RefundModel,refund_id)
    if not refund:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Refund not found.")
    if current_user.role == UserRole.CUSTOMER:
        if refund.order.customer.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed to access.")
    return refund

def get_all_refund(db:Session,skip:int=0,limit:int=100)->list[RefundModel]:
    refunds = db.scalars(select(RefundModel).offset(skip).limit(limit)).all()
    return refunds


    