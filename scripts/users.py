from scripts.database import get_session

from src.users.service import create_user, update_user_role
from src.users.dtos import UserCreateSchema, UserRoleUpdateSchema
from src.common.enum import UserRole

def seed_users():
    db = get_session()

    print("Seeding users...")

    admin = create_user(
        UserCreateSchema(
            username="admin",
            email="admin@retail.com",
            password="Admin@123",
        ),
        db,
    ) 
    update_user_role(
        admin.id,
        UserRoleUpdateSchema(
            role=UserRole.ADMIN
        ),
        db,
    )

    analyst = create_user(
        UserCreateSchema(
            username="analyst",
            email="analyst@retail.com",
            password="Analyst@123",
        ),
        db,
    ) 
    update_user_role(
        analyst.id,
        UserRoleUpdateSchema(
            role=UserRole.BUSINESS_ANALYST
        ),
        db,
    )
    inventory = create_user(
        UserCreateSchema(
            username="inventory",
            email="inventory@retail.com",
            password="Inventory@123",
        ),
        db,
    )
    update_user_role(
        inventory.id,
        UserRoleUpdateSchema(
            role=UserRole.INVENTORY_MANAGER
        ),
        db,
    )
    for i in range(1, 51):
        create_user(
            UserCreateSchema(
                username=f"customer{i}",
                email=f"customer{i}@retail.com",
                password="Customer@123",
            ),
            db,
        )

    db.close()

    print("✅ Users seeded successfully.")        
                 