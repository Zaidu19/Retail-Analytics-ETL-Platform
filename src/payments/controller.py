
from fastapi import APIRouter,Depends,status,Query  
from sqlalchemy.orm import Session
from uuid import UUID

from src.users.models import UserModel
from src.common.enum import UserRole
from src.auth.service import require_roles

from src.db.database import get_db
from src.payments.dtos import(
    PaymentUpdateSchema,
    PaymentResponseSchema
)
from src.payments.service import(
    update_payment_status,
    get_payment_by_id,
    get_list_of_payments,
)

router = APIRouter(prefix="/payments",tags=["Payments"])


@router.patch("/{payment_id}",response_model=PaymentResponseSchema,status_code=status.HTTP_200_OK)
def update_status_endpoint(payment_id:UUID,payload:PaymentUpdateSchema,
                           db:Session=Depends(get_db),
                           _:UserModel=Depends(require_roles(UserRole.ADMIN))):
    return update_payment_status(payment_id,payload,db)

@router.get("/{payment_id}",response_model=PaymentResponseSchema,status_code=status.HTTP_200_OK)
def get_payment_by_id_endpoint(payment_id:UUID,db:Session=Depends(get_db),
                               current_user:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST,UserRole.CUSTOMER))):
    return get_payment_by_id(payment_id,current_user,db)

@router.get("/",response_model=list[PaymentResponseSchema],status_code=status.HTTP_200_OK)
def get_list_of_payments_endpoint(db:Session=Depends(get_db),
                                  skip:int=Query(0,ge=0),limit:int=Query(100,ge=1,le=100),
                                  _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_list_of_payments(db,skip,limit)