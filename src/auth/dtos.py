
from pydantic import BaseModel

class LoginSchema(BaseModel):
    email:str
    password:str

class TokenResponseSchema(BaseModel):
    access_token:str
    token_type:str ="bearer"    