from fastapi import status


def test_create_customer(client, customer_headers):

    payload = {
        "full_name": "Test Customer",
        "phone_number": "9999999999",
        "country": "India",
        "city": "Lucknow",
    }

    response = client.post(
        "/customers/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()

    assert body["full_name"] == payload["full_name"]
    assert body["country"] == payload["country"]
    assert body["city"] == payload["city"]

def test_create_customer_profile_twice(
    client,
    customer_headers,
    customer_profile,
):

    payload = {
        "full_name": "Another Customer",
        "phone_number": "8888888888",
        "country": "India",
        "city": "Delhi",
    }

    response = client.post(
        "/customers/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Customer profile already exist."

def test_get_my_profile(
    client,
    customer_headers,
    customer_profile,
):

    response = client.get(
        "/customers/me",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["full_name"] == customer_profile["full_name"]
    assert body["country"] == customer_profile["country"]

def test_update_my_profile(
    client,
    customer_headers,
    customer_profile,
):

    payload = {
        "full_name": "Updated Customer",
        "phone_number": "7777777777",
        "country": "India",
        "city": "Mumbai",
    }

    response = client.put(
        "/customers/me",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["full_name"] == "Updated Customer"
    assert body["city"] == "Mumbai"

def test_admin_can_get_all_customers(
    client,
    admin_headers,
    customer_profile,
):

    response = client.get(
        "/customers/",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    customers = response.json()

    assert len(customers) >= 1    


def test_business_analyst_can_get_all_customers(
    client,
    business_analyst_headers,
    customer_profile,
):

    response = client.get(
        "/customers/",
        headers=business_analyst_headers,
    )

    assert response.status_code == status.HTTP_200_OK

def test_customer_cannot_get_all_customers(
    client,
    customer_headers,
):

    response = client.get(
        "/customers/",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_customer_by_id(
    client,
    admin_headers,
    customer_profile,
):

    response = client.get(
        f"/customers/{customer_profile['id']}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["id"] == customer_profile["id"]

from uuid import uuid4

def test_get_invalid_customer(
    client,
    admin_headers,
):

    response = client.get(
        f"/customers/{uuid4()}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND    
                