import pytest
from fastapi import status


@pytest.fixture
def refund(
    client,
    customer_headers,
    completed_order,
):

    payload = {
        "order_id": completed_order["id"],
        "reason": "Received damaged product."
    }

    response = client.post(
        "/refunds/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    return response.json()