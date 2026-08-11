import pytest
from fastapi import status


import pytest
from fastapi import status


@pytest.fixture
def pending_order(
    client,
    customer_headers,
    customer_profile,
    product,
):

    payload = {
        "payment_method": "cash",
        "items": [
            {
                "product_id": product["id"],
                "quantity": 2,
            }
        ]
    }

    response = client.post(
        "/orders/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    return response.json()

@pytest.fixture
def paid_order(
    client,
    admin_headers,
    payment,
    pending_order,
):

    response = client.patch(
        f"/payments/{payment.id}",
        json={
            "payment_status": "success"
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    return pending_order

@pytest.fixture
def shipped_order(
    client,
    admin_headers,
    paid_order,
):

    response = client.patch(
        f"/orders/{paid_order['id']}/status",
        json={
            "status": "shipped"
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    return response.json()


@pytest.fixture
def delivered_order(
    client,
    admin_headers,
    shipped_order,
):

    response = client.patch(
        f"/orders/{shipped_order['id']}/status",
        json={
            "status": "delivered"
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    return response.json()

@pytest.fixture
def completed_order(
    client,
    admin_headers,
    delivered_order,
):

    response = client.patch(
        f"/orders/{delivered_order['id']}/status",
        json={
            "status": "completed"
        },
        headers=admin_headers,
    )

    assert response.status_code == 200

    return response.json()
