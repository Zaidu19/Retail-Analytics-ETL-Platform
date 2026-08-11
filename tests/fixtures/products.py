import pytest
from fastapi import status


@pytest.fixture
def product(client, admin_headers, category):

    payload = {
        "name": "iPhone 16",
        "description": "Latest Apple smartphone with advanced camera and performance.",
        "category_id": category["id"],
        "price": "99999.99",
        "cost": "80000.00",
        "stock_qty": 20,
    }

    response = client.post(
        "/products/",
        json=payload,
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    return response.json()