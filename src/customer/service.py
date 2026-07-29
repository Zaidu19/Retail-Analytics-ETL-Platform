from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.customer.dtos import CustomerCreateSchema,CustomerUpdateSchema,CustomerResponseSchema
from src.customer.models import CustomerModel

def create_customer(payload: CustomerCreateSchema,db: Session,)->CustomerModel:

    existing_customer = db.scalar(
        select(CustomerModel).where(
            CustomerModel.email == payload.email
        )
    )

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this email already exists",
        )

    customer = CustomerModel(
        **payload.model_dump()
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer

def get_all_customers(db:Session,)-> list[CustomerModel]:
    customers = db.scalars(select(CustomerModel)).all()
    return customers

def get_customer_with_id(customer_id:str,db:Session,)->CustomerModel:
    customer =db.get(CustomerModel,customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="customer not found")
    return customer

def update_customer(customer_id:str,payload:CustomerUpdateSchema,db:Session)->CustomerModel:
    customer = db.get(CustomerModel,customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="customer not found")
    customer.full_name = payload.full_name
    customer.phone_number = payload.phone_number
    customer.country = payload.country
    customer.city = payload.city
    customer.is_active = payload.is_active

    db.commit()
    db.refresh(customer)

    return customer

def delete_customer(customer_id:str,db:Session,)->dict[str,str]:
    customer= db.get(CustomerModel,customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="customer not found")
    
    db.delete(customer)
    db.commit()

