from datetime import datetime,date
from uuid import UUID

from pydantic import BaseModel,EmailStr,Field,ConfigDict

class CustomerCreateSchema(BaseModel):
    full_name :str =Field(...,min_length=2,max_length=255)
    email :EmailStr
    phone_number:str | None = Field(default=None,max_length=20)
    country:str =Field(...,max_length=100)
    city :str = Field(...,max_length=100)
    signup_date:date
    is_active :bool = True

    model_config = ConfigDict(from_attributes=True)

class CustomerUpdateSchema(BaseModel):
    full_name:str | None =Field(default=None,min_length=2,max_length=255)
    phone_number :str |None = Field(default=None,max_length=20)
    country :str|None = Field(default=None,max_length=100)
    city:str|None = Field(default=None,max_length=100)
    is_active:bool |None = None

    model_config = ConfigDict(from_attributes=True)

class CustomerResponseSchema(BaseModel):
    id:UUID
    full_name:str
    email:str
    phone_number:str|None
    country:str
    city:str
    signup_date:date
    is_active :bool
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)    