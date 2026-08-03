
from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.auth.dtos import TokenResponseSchema,LoginSchema
from src.auth.service import login

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/",response_model=TokenResponseSchema,status_code=status.HTTP_200_OK)
def login_endpoint(payload:LoginSchema,db:Session=Depends(get_db)):
    return login(payload,db)

