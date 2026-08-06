
from uuid import UUID
from pydantic import BaseModel,ConfigDict
from decimal import Decimal
from datetime import datetime

from src.common.enum import RefundStatus
class RefundCreateSchema(BaseModel):
    order_id:UUID
    reason:str

class RefundResponseSchema(BaseModel):
    id:UUID
    order_id:UUID
    amount:Decimal
    reason:str
    status:RefundStatus
    requested_at:datetime
    processed_at:datetime|None 

    model_config=ConfigDict(from_attributes=True)   
