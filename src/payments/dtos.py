
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel,ConfigDict
from src.common.enum import PaymentStatus,PaymentMethod


class PaymentCreateSchema(BaseModel):
    order_id:UUID
    payment_method:PaymentMethod


class PaymentUpdateSchema(BaseModel):
    payment_status:PaymentStatus

    model_config=ConfigDict(from_attributes=True)


class PaymentResponseSchema(BaseModel):
    id:UUID
    order_id:UUID
    amount:Decimal
    payment_method:PaymentMethod
    payment_status:PaymentStatus
    paid_at:datetime|None
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes= True)  

