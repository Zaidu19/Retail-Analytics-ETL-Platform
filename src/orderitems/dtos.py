from pydantic import BaseModel,ConfigDict,Field
from uuid import UUID
from decimal import Decimal
from datetime import datetime


class OrderItemCreateSchema(BaseModel):
    order_id:UUID
    product_id:UUID
    quantity:int = Field(gt=0)

    model_config =ConfigDict(from_attributes=True)

class OrderItemResponseSchema(BaseModel):
    id:UUID
    order_id:UUID
    product_id:UUID
    quantity:int
    unit_price:Decimal   
    created_at:datetime
    updated_at:datetime

    model_config =ConfigDict(from_attributes=True)

class OrderItemUpdateSchema(BaseModel):
    quantity:int=Field(gt=0)    
