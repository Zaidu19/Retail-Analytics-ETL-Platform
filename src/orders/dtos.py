from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel,ConfigDict,Field

from src.common.enum import OrderStatus,PaymentMethod
class OrderItemInputSchema(BaseModel):
    product_id:UUID
    quantity:int = Field(...,gt=0)

class OrderCreateSchema(BaseModel):
    payment_method:PaymentMethod
    items:list[OrderItemInputSchema]

    model_config=ConfigDict(from_attributes=True)

class OrderUpdateSchema(BaseModel):
    status:OrderStatus  

    model_config=ConfigDict(from_attributes=True)  

class OrderResponseSchema(BaseModel):
    id:UUID
    customer_id:UUID    
    status:OrderStatus
    grand_total:Decimal

    model_config=ConfigDict(from_attributes=True)

class CustomerOrdersResponseSchema(BaseModel):
    id:UUID
    order_date:date
    status:OrderStatus
    grand_total:Decimal
    model_config=ConfigDict(from_attributes=True)
    