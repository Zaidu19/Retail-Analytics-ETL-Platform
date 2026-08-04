from uuid import UUID

from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session

from src.customers.dtos import(
    CustomerCreateSchema,
    CustomerResponseSchema,
    CustomerUpdateSchema,
)
from src.customers.service import(
    create_customer,
    get_all_customers,
    get_customer_with_id,
    update_customer,
    delete_customer,
)
from src.auth.service import require_roles
from src.users.models import UserModel
from src.common.enum import UserRole

from src.db.database import get_db
from src.orders.service import get_orders_by_customer
from src.orders.dtos import OrderResponseSchema

router = APIRouter(prefix="/customers",tags=["Customers"])

@router.post("/",response_model=CustomerResponseSchema,status_code=status.HTTP_201_CREATED)
def create_customer_endpoint(payload:CustomerCreateSchema,
                             db:Session=Depends(get_db),
                             current_user:UserModel=Depends(require_roles(UserRole.CUSTOMER))):
    return create_customer(payload,current_user,db)

@router.get("/",response_model=list[CustomerResponseSchema],status_code=status.HTTP_200_OK)
def get_all_customer_endpoint(db:Session=Depends(get_db),
                              _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_all_customers(db)

@router.get("/{customer_id}",response_model=CustomerResponseSchema,status_code=status.HTTP_200_OK)
def get_customer_by_id_endpoint(customer_id:UUID,db:Session=Depends(get_db),
                                _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_customer_with_id(customer_id,db)

@router.put("/{customer_id}",response_model=CustomerResponseSchema,status_code=status.HTTP_200_OK)
def update_customer_endpoint(customer_id:UUID,payload:CustomerUpdateSchema,
                             db:Session=Depends(get_db),
                             _:UserModel=Depends(require_roles(UserRole.ADMIN))):
    return update_customer(customer_id,payload,db)

@router.delete("/{customer_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_customer_endpoint(customer_id:UUID,db:Session=Depends(get_db),
                             _:UserModel=Depends(require_roles(UserRole.ADMIN))):
    return delete_customer(customer_id,db)

@router.get("/{customer_id}/orders",response_model=list[OrderResponseSchema],status_code=status.HTTP_200_OK)
def get_orders_by_customer_id_endpoint(customer_id:UUID,db:Session=Depends(get_db),
                                       _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_orders_by_customer(customer_id,db)
