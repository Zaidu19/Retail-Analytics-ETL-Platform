
from uuid import UUID
from fastapi import HTTPException,status
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from src.users.models import UserModel
from src.users.dtos import UserCreateSchema,UserRoleUpdateSchema
from src.auth.security import hash_password
from src.common.enum import UserRole

def create_user(payload:UserCreateSchema,db:Session)->UserModel:
    try:
        existing_user = db.scalar(select(UserModel).where(UserModel.username == payload.username))
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists.")

        existing_email=db.scalar(select(UserModel).where(UserModel.email == payload.email))
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exist.")

        password_hash = hash_password(payload.password)

        user = UserModel(
            username =payload.username,
            email = payload.email,
            password_hash = password_hash,
            role = UserRole.CUSTOMER
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
        
    except Exception:
        db.rollback()
        raise    

def update_user_role(user_id: UUID,payload: UserRoleUpdateSchema,db: Session,) -> UserModel:

    user = db.get(UserModel, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    if user.role == payload.role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User is already {payload.role.value}."
            )
    
    if (
    user.role == UserRole.ADMIN
    and payload.role != UserRole.ADMIN):
        
        admin_count = db.scalar(
            select(func.count(UserModel.id))
            .where(UserModel.role == UserRole.ADMIN)
        )

        if admin_count == 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove the last admin."
            )
    user.role = payload.role

    db.commit()
    db.refresh(user)

    return user    