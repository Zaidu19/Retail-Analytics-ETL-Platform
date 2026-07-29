from uuid import UUID
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel,ConfigDict,Field
class ProductCreateSchema(BaseModel):
    name : str = Field(min_length=2,max_length=100,)
    description :str|None= Field(default=None,min_length=20,max_length=500,)
    category_id:UUID
    price:Decimal = Field(gt=0,decimal_places=2,)
    cost:Decimal = Field(ge=0,decimal_places=2,)
    stock_qty:int =Field(ge=0,)

    model_config = ConfigDict(from_attributes=True)

class ProductUpdateSchema(BaseModel):
    name:str|None =Field(default=None,min_length=2,max_length=100,)
    description:str|None = Field(default=None,min_length=20,max_length=500,)
    category_id:UUID |None =None
    price:Decimal|None =Field(default=None,gt=2,decimal_places=2,)
    cost:Decimal|None = Field(default=None,ge=0,decimal_places=2,)
    stock_qty:int|None = Field(default=None,ge=0,)

    model_config=ConfigDict(from_attributes=True)

class ProductResponseSchema(BaseModel):
    id:UUID
    name:str
    description:str|None
    category_id:UUID
    price:Decimal
    cost:Decimal
    stock_qty:int
    created_at:datetime 
    updated_at:datetime

    model_config=ConfigDict(from_attributes=True)
       


