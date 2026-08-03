
from fastapi import HTTPException,status,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.auth.dtos import LoginSchema,TokenResponseSchema
from src.db.database import get_db
from src.common.enum import UserRole
from src.users.models import UserModel
from src.auth.security import (
    create_access_token,
    verify_password,
    oauth2_scheme,
    decode_access_token,
)

def login(payload:LoginSchema,db:Session)->TokenResponseSchema:
    user = db.scalars(select(UserModel).where(UserModel.email == payload.email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password.")

    if not verify_password(payload.password,user.password_hash,):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password.")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User account is inactive.")

    token = create_access_token(
        {
        "sub":str(user.id),
        "role":user.role.value
        }
    )

    return {
        "access_token":token,
        "token_type":"bearer"
    }

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db))->UserModel:

    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials.")

    user = db.get(UserModel,user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found.")

    return user

def get_current_admin(current_user:UserModel = Depends(get_current_user))->UserModel:

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only admins can perform this action.")

    return current_user

def get_current_inventory_manager(current_user:UserModel=Depends(get_current_user))->UserModel:
    if current_user.role != UserRole.INVENTORY_MANAGER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only inventory_manager can perform this action")

    return current_user

def get_current_business_analayst(current_user:UserModel=Depends(get_current_user))->UserModel:
    if current_user.role != UserRole.BUSINESS_ANALYST:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only business_analyst can perform this action.")

    return current_user

def get_current_customer(current_user:UserModel=Depends(get_current_user))->UserModel:
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only customers can perform this action.")

    return current_user



    
     
    