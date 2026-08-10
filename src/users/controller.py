
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import status,Depends,APIRouter
from src.db.database import get_db
from src.users.dtos import UserCreateSchema,UserResponseSchema,UserRoleUpdateSchema
from src.users.service import create_user,update_user_role
from src.auth.service import require_roles
from src.users.models import UserModel
from src.common.enum import UserRole


router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED,
             summary="Register User",
            description="Registers a new user account. Every newly registered user is automatically assigned the CUSTOMER role.")
def create_user_endpoint(payload:UserCreateSchema,db:Session=Depends(get_db)):
    return create_user(payload,db) 

@router.patch("/{user_id}/role",response_model=UserResponseSchema,status_code=status.HTTP_200_OK,
              summary="Update User Role",
              description="Allows an administrator to change a user's role (CUSTOMER, BUSINESS_ANALYST,INVENTORY_MANAGER or ADMIN). Prevents removing the last remaining administrator.")
def update_user_role_endpoint(user_id: UUID,payload: UserRoleUpdateSchema,
                              db: Session = Depends(get_db), 
                              _: UserModel = Depends(require_roles(UserRole.ADMIN)),):
    return update_user_role(user_id, payload, db)