from pydantic import BaseModel,ConfigDict,Field
from uuid import UUID
from decimal import Decimal
from datetime import datetime




class OrderItemResponseSchema(BaseModel):
    id:UUID
    order_id:UUID
    product_id:UUID
    quantity:int
    unit_price:Decimal   
    created_at:datetime
    updated_at:datetime

    model_config =ConfigDict(from_attributes=True)

 
