
from uuid import UUID

from pydantic import BaseModel,ConfigDict,EmailStr
from src.common.enum import UserRole

class UserCreateSchema(BaseModel):
    username :str
    email:EmailStr
    password: str
    role :UserRole

class UserLoginSchema(BaseModel):
    email:str
    password:str

class UserResponseSchema(BaseModel):
    id:UUID
    username:str
    email:EmailStr
    role:UserRole
    is_active: bool            

    model_config = ConfigDict(from_attributes=True)
    