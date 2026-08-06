from uuid import UUID
from fastapi import APIRouter,status,Depends,Query
from sqlalchemy.orm import Session

from src.users.models import UserModel
from src.auth.service import require_roles
from src.common.enum import UserRole
from src.db.database import get_db
from src.refund.dtos import(
    RefundCreateSchema,
    RefundResponseSchema,
)

from src.refund.service import(
    create_refund,
    approve_refund,
    reject_refund,
    get_all_refund,
    get_refund_by_id,
)

router = APIRouter(prefix="/refunds",tags=["Refund"])

@router.post("/",response_model=RefundResponseSchema,status_code=status.HTTP_201_CREATED)
def create_refund_endpoint(payload:RefundCreateSchema,current_user:UserModel=Depends(require_roles(UserRole.CUSTOMER)),
                           db:Session=Depends(get_db)):
    return create_refund(payload,current_user,db)

@router.patch("/{refund_id}/approve",response_model=RefundResponseSchema,status_code=status.HTTP_200_OK)
def approve_refund_endpoint(refund_id:UUID,db:Session=Depends(get_db),_:UserModel=Depends(require_roles(UserRole.ADMIN))):
    return approve_refund(refund_id,db)

@router.patch("/{refund_id}/reject",response_model=RefundResponseSchema,status_code=status.HTTP_200_OK)
def reject_refund_endpoint(refund_id:UUID,db:Session=Depends(get_db),_:UserModel=Depends(require_roles(UserRole.ADMIN))):
    return reject_refund(refund_id,db)

@router.get("/{refund_id}",response_model=RefundResponseSchema,status_code=status.HTTP_200_OK)
def get_refund_by_id_endpoint(refund_id:UUID,current_user:UserModel=Depends(require_roles(UserRole.CUSTOMER,
                            UserRole.BUSINESS_ANALYST,UserRole.ADMIN)),db:Session=Depends(get_db)):
    return get_refund_by_id(refund_id,current_user,db)

@router.get("/",response_model=list[RefundResponseSchema],status_code=status.HTTP_200_OK)
def get_all_refund_endpoint(db:Session=Depends(get_db),skip:int=Query(0,ge=0),limit:int=Query(100,ge=1,le=100),
                            _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_all_refund(db,skip,limit)
