from uuid import UUID

from datetime import date
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.customers.dtos import CustomerCreateSchema,CustomerUpdateSchema
from src.customers.models import CustomerModel
from src.users.models import UserModel

def create_customer(payload: CustomerCreateSchema,current_user:UserModel,db: Session,)->CustomerModel:

    existing_customer = db.scalar(
        select(CustomerModel).where(
            CustomerModel.user_id == current_user.id
        )
    )

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer profile already exist.",
        )

    customer = CustomerModel(
        full_name = payload.full_name,
        email = current_user.email,
        phone_number = payload.phone_number,
        country = payload.country,
        city = payload.city,
        signup_date = date.today(),
        is_active = True,
        user_id = current_user.id
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

def delete_customer(customer_id:str,db:Session,)->None:
    customer= db.get(CustomerModel,customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="customer not found")
    
    db.delete(customer)
    db.commit()

