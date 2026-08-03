
from sqlalchemy.orm import Session
from fastapi import status,Depends,APIRouter
from src.db.database import get_db
from src.users.dtos import UserCreateSchema,UserResponseSchema
from src.users.service import create_user


router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def create_user_endpoint(payload:UserCreateSchema,db:Session=Depends(get_db)):
    return create_user(payload,db) 