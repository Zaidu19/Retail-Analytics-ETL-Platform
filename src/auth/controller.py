
from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from src.db.database import get_db
from src.auth.dtos import TokenResponseSchema
from src.auth.service import login

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/login",response_model=TokenResponseSchema,status_code=status.HTTP_200_OK,
            summary="User Login",
            description="Authenticates a registered user and returns a JWT access token for accessing protected endpoints.")
def login_endpoint(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    return login(form_data,db)

