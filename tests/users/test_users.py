from fastapi import status
from src.common.enum import UserRole

from fastapi import status


def test_create_user(client):

    payload = {
        "username": "zaid123",
        "email": "zaid@test.com",
        "password": "Password@123"
    }

    response = client.post(
        "/users/",
        json=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()

    assert body["username"] == payload["username"]
    assert body["email"] == payload["email"]
    assert body["role"] == "customer"
    assert body["is_active"] is True

def test_duplicate_username(client, customer_user):

    payload = {
        "username": customer_user.username,
        "email": "new@test.com",
        "password": "Password@123"
    }

    response = client.post(
        "/users/",
        json=payload,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == "Username already exists."

def test_duplicate_email(client, customer_user):

    payload = {
        "username": "anotheruser",
        "email": customer_user.email,
        "password": "Password@123"
    }

    response = client.post(
        "/users/",
        json=payload,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == "Email already exist."        


def test_update_user_role_success(
    client,
    admin_headers,
    customer_user,
):

    response = client.patch(
        f"/users/{customer_user.id}/role",
        json={
            "role": UserRole.BUSINESS_ANALYST.value
        },
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["role"] == UserRole.BUSINESS_ANALYST.value


def test_update_user_role_success(
    client,
    admin_headers,
    customer_user,
):

    response = client.patch(
        f"/users/{customer_user.id}/role",
        json={
            "role": UserRole.BUSINESS_ANALYST.value
        },
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["role"] == UserRole.BUSINESS_ANALYST.value    


def test_customer_cannot_update_user_role(
    client,
    customer_headers,
    admin_user,
):

    response = client.patch(
        f"/users/{admin_user.id}/role",
        json={
            "role": UserRole.CUSTOMER.value
        },
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN  

def test_update_same_role(
    client,
    admin_headers,
    customer_user,
):

    response = client.patch(
        f"/users/{customer_user.id}/role",
        json={
            "role": UserRole.CUSTOMER.value
        },
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User is already customer."

def test_cannot_remove_last_admin(
    client,
    admin_headers,
    admin_user,
):

    response = client.patch(
        f"/users/{admin_user.id}/role",
        json={
            "role": UserRole.CUSTOMER.value
        },
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Cannot remove the last admin."