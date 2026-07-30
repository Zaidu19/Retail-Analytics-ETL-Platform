from datetime import date
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel,ConfigDict

from src.common.enum import OrderStatus

class OrderCreateSchema(BaseModel):
    customer_id:UUID

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
    