import pytest

from src.users.models import UserModel
from src.auth.security import hash_password
from src.common.enum import UserRole

@pytest.fixture()
def customer_user(db):

    user = UserModel(
        username="testcustomer",
        email="customer@test.com",
        password_hash=hash_password("Password@123"),
        role=UserRole.CUSTOMER,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture()
def admin_user(db):      
    user = UserModel(
        username="adminuser",
        email="adminuser@gmail.com",
        password_hash =hash_password("Password@123"),
        role=UserRole.ADMIN,
        is_active = True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@pytest.fixture()
def business_analyst_user(db):

    user = UserModel(
        username="analyst",
        email="analyst@test.com",
        password_hash=hash_password("Password@123"),
        role=UserRole.BUSINESS_ANALYST,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@pytest.fixture
def inventory_manager_user(db):

    user = UserModel(
        username="inventory",
        email="inventory@test.com",
        password_hash=hash_password("Password@123"),
        role=UserRole.INVENTORY_MANAGER,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
