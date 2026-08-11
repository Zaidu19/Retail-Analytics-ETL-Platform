from fastapi import status


def test_admin_get_payment_by_id(
    client,
    admin_headers,
    payment,
):

    response = client.get(
        f"/payments/{payment.id}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["id"] == str(payment.id)


def test_customer_get_own_payment(
    client,
    customer_headers,
    payment,
):

    response = client.get(
        f"/payments/{payment.id}",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_200_OK

from uuid import uuid4


def test_invalid_payment(
    client,
    admin_headers,
):

    response = client.get(
        f"/payments/{uuid4()}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert response.json()["detail"] == "Payment not found."

def test_list_payments(
    client,
    admin_headers,
    payment,
):

    response = client.get(
        "/payments/",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) >= 1

def test_customer_cannot_list_payments(
    client,
    customer_headers,
):

    response = client.get(
        "/payments/",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_complete_payment(
    client,
    admin_headers,
    payment,
):

    response = client.patch(
        f"/payments/{payment.id}",
        json={
            "payment_status": "success"
        },
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["payment_status"] == "success"
    assert body["paid_at"] is not None

def test_payment_already_success(
    client,
    admin_headers,
    payment,
):

    client.patch(
        f"/payments/{payment.id}",
        json={
            "payment_status": "success"
        },
        headers=admin_headers,
    )

    response = client.patch(
        f"/payments/{payment.id}",
        json={
            "payment_status": "success"
        },
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == "Payment already has this status."

def test_mark_payment_failed(
    client,
    admin_headers,
    payment,
):

    response = client.patch(
        f"/payments/{payment.id}",
        json={
            "payment_status": "failed"
        },
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["payment_status"] == "failed"

def test_invalid_payment_transition(
    client,
    admin_headers,
    payment,
):

    client.patch(
        f"/payments/{payment.id}",
        json={
            "payment_status": "success"
        },
        headers=admin_headers,
    )

    response = client.patch(
        f"/payments/{payment.id}",
        json={
            "payment_status": "failed"
        },
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST  

def test_payment_marks_order_paid(
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

    assert response.status_code == status.HTTP_200_OK

    order = client.get(
        f"/orders/{pending_order['id']}",
        headers=admin_headers,
    ).json()

    assert order["status"] == "paid"                  
               