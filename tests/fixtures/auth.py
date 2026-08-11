import pytest

import pytest


def get_auth_headers(client, email, password):

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def customer_headers(client, customer_user):
    return get_auth_headers(
        client,
        customer_user.email,
        "Password@123",
    )


@pytest.fixture
def admin_headers(client, admin_user):
    return get_auth_headers(
        client,
        admin_user.email,
        "Password@123",
    )


@pytest.fixture
def business_analyst_headers(client, business_analyst_user):
    return get_auth_headers(
        client,
        business_analyst_user.email,
        "Password@123",
    )


@pytest.fixture
def inventory_manager_headers(client, inventory_manager_user):
    return get_auth_headers(
        client,
        inventory_manager_user.email,
        "Password@123",
    )
