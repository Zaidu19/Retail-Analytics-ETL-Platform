import pytest
from fastapi import status
@pytest.fixture()
def customer_profile(client, customer_headers):

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

    return response.json()
