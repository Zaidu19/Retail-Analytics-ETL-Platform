from scripts.database import get_session
from scripts.utils import fake

from sqlalchemy import select

from src.users.models import UserModel
from src.customers.service import create_customer
from src.customers.dtos import CustomerCreateSchema
from src.common.enum import UserRole

def seed_customers():
    db = get_session()

    print("Seeding customers...")

    users = db.scalars(
        select(UserModel).where(
            UserModel.role == UserRole.CUSTOMER
        )
    ).all()

    for user in users:
        create_customer(
            CustomerCreateSchema(
                full_name=fake.name(),
                phone_number=fake.numerify("############"),
                country=fake.country(),
                city=fake.city(),
            ),
            user,
            db,
        )            
    db.close()

    print("✅ Customers seeded successfully.")