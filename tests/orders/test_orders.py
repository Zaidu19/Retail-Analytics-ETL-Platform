from fastapi import status
from uuid import uuid4

def test_create_order(
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

    body = response.json()

    assert body["customer_id"] == customer_profile["id"]
    assert body["status"] == "pending"
    assert float(body["grand_total"]) > 0




def test_create_order_invalid_product(
    client,
    customer_headers,
    customer_profile,
):

    payload = {
        "payment_method": "cash",
        "items": [
            {
                "product_id": str(uuid4()),
                "quantity": 2,
            }
        ]
    }

    response = client.post(
        "/orders/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST   

def test_create_order_insufficient_stock(
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
                "quantity": 999,
            }
        ]
    }

    response = client.post(
        "/orders/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_customer_without_profile_cannot_create_order(
    client,
    customer_headers,
    product,
):

    payload = {
        "payment_method": "cash",
        "items": [
            {
                "product_id": product["id"],
                "quantity": 1,
            }
        ]
    }

    response = client.post(
        "/orders/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Please create your customer profile first."


def test_create_order_invalid_quantity(
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
                "quantity": 0,
            }
        ]
    }

    response = client.post(
        "/orders/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_admin_can_get_all_orders(
    client,
    admin_headers,
    pending_order,
):

    response = client.get(
        "/orders/",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 1


def test_business_analyst_can_get_all_orders(
    client,
    business_analyst_headers,
    pending_order,
):

    response = client.get(
        "/orders/",
        headers=business_analyst_headers,
    )

    assert response.status_code == status.HTTP_200_OK


def test_customer_cannot_get_all_orders(
    client,
    customer_headers,
):

    response = client.get(
        "/orders/",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_customer_can_get_own_order(
    client,
    customer_headers,
    pending_order,
):

    response = client.get(
        f"/orders/{pending_order['id']}",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["id"] == pending_order["id"]

from uuid import uuid4

def test_get_invalid_order(
    client,
    admin_headers,
):

    response = client.get(
        f"/orders/{uuid4()}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Order not found."


def test_cannot_manually_mark_order_paid(
    client,
    admin_headers,
    pending_order,
):

    response = client.patch(
        f"/orders/{pending_order['id']}/status",
        json={"status": "paid"},
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_cannot_ship_pending_order(
    client,
    admin_headers,
    pending_order,
):

    response = client.patch(
        f"/orders/{pending_order['id']}/status",
        json={"status": "shipped"},
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_cancel_pending_order(
    client,
    admin_headers,
    pending_order,
):

    response = client.patch(
        f"/orders/{pending_order['id']}/cancel",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["status"] == "cancelled"



def test_cancel_invalid_order(
    client,
    admin_headers,
):

    response = client.patch(
        f"/orders/{uuid4()}/cancel",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert response.json()["detail"] == "Order not found."                                           


def test_cancel_already_cancelled_order(
    client,
    admin_headers,
    pending_order,
):

    response = client.patch(
        f"/orders/{pending_order['id']}/cancel",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    response = client.patch(
        f"/orders/{pending_order['id']}/cancel",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == "Order already cancelled."

def test_customer_cannot_cancel_order(
    client,
    customer_headers,
    pending_order,
):

    response = client.patch(
        f"/orders/{pending_order['id']}/cancel",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_business_analyst_cannot_cancel_order(
    client,
    business_analyst_headers,
    pending_order,
):

    response = client.patch(
        f"/orders/{pending_order['id']}/cancel",
        headers=business_analyst_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN  

def test_paid_order_can_be_shipped(
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

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "shipped"

def test_shipped_order_can_be_delivered(
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

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "delivered"

def test_delivered_order_can_be_completed(
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

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "completed"


def test_cannot_cancel_paid_order(
    client,
    admin_headers,
    paid_order,
):

    response = client.patch(
        f"/orders/{paid_order['id']}/cancel",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == "Paid orders must be refunded before cancellation."

def test_cannot_cancel_shipped_order(
    client,
    admin_headers,
    shipped_order,
):

    response = client.patch(
        f"/orders/{shipped_order['id']}/cancel",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == "Cannot cancel shipped or delivered orders."

def test_cannot_cancel_delivered_order(
    client,
    admin_headers,
    delivered_order,
):

    response = client.patch(
        f"/orders/{delivered_order['id']}/cancel",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == "Cannot cancel shipped or delivered orders."

def test_completed_order_cannot_change_status(
    client,
    admin_headers,
    completed_order,
):

    response = client.patch(
        f"/orders/{completed_order['id']}/status",
        json={
            "status": "shipped"
        },
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST                                   