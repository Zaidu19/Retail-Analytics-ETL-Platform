
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel,ConfigDict

from src.common.enum import InventoryReason

class InventoryLogCreateSchema(BaseModel):

    product_id:UUID
    change_qty:int
    reason:InventoryReason

    model_config=ConfigDict(from_attributes=True)

class InventoryLogResponseSchema(BaseModel):
    id:UUID
    product_id:UUID
    change_qty:int
    reason :InventoryReason
    created_at:datetime
    updated_at:datetime    

    model_config=ConfigDict(from_attributes=True)