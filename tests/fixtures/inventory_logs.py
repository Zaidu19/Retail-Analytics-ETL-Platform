import pytest
from fastapi import status


@pytest.fixture
def inventory_log(
    client,
    inventory_manager_headers,
    product,
):

    payload = {
        "product_id": product["id"],
        "change_qty": 10,
        "reason": "restock",
    }

    response = client.post(
        "/inventory_logs/",
        json=payload,
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    return response.json()