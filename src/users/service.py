
from fastapi import HTTPException,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.users.models import UserModel
from src.users.dtos import UserCreateSchema
from src.auth.security import hash_password

def create_user(payload:UserCreateSchema,db:Session)->UserModel:
    try:
        existing_user = db.scalars(select(UserModel).where(UserModel.username == payload.username)).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists.")

        existing_email=db.scalars(select(UserModel).where(UserModel.email == payload.email)).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exist.")

        password_hash = hash_password(payload.password)

        user = UserModel(
            username =payload.username,
            email = payload.email,
            password_hash = password_hash,
            role = payload.role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
        
    except Exception:
        db.rollback()
        raise    