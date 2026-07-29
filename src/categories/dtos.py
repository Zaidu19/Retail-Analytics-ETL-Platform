from uuid import UUID
from datetime import datetime

from pydantic import BaseModel,Field,ConfigDict


class CategoryCreateSchema(BaseModel):
    name : str =Field(...,min_length=2,max_length=255)
    description :str = Field(...,min_length=25,max_length=1000)

    model_config = ConfigDict(from_attributes=True)

class CategoryUpdateSchema(BaseModel):
    name:str | None =Field(default=None,min_length=2,max_length=255)
    description :str |None = Field(default=None,min_length=25,max_length=500)

class CategoryResponseSchema(BaseModel):
    id : UUID
    name:str
    description:str
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)       