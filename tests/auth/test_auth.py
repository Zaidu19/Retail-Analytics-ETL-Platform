from fastapi import status


def test_login_success(client,customer_user):
    response = client.post(
        "/auth/login",
        data={
            "username": customer_user.email,
            "password": "Password@123",
        },
    )

    assert response.status_code  == status.HTTP_200_OK

def test_login_invalid_password(client, customer_user):

    response = client.post(
        "/auth/login",
        data={
            "username": customer_user.email,
            "password": "WrongPassword",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_login_invalid_email(client):

    response = client.post(
        "/auth/login",
        data={
            "username": "unknown@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_missing_password(client):

    response = client.post(
        "/auth/login",
        data={
            "username": "customer@test.com",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_login_missing_username(client):

    response = client.post(
        "/auth/login",
        data={
            "password": "Password@123",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY                