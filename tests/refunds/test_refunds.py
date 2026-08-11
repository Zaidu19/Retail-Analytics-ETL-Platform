from fastapi import status

def test_create_refund(
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

    body = response.json()

    assert body["status"] == "pending"

from uuid import uuid4

def test_create_refund_invalid_order(
    client,
    customer_headers,
):

    payload = {
        "order_id": str(uuid4()),
        "reason": "Wrong product."
    }

    response = client.post(
        "/refunds/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_duplicate_refund(
    client,
    customer_headers,
    refund,
):

    payload = {
        "order_id": refund["order_id"],
        "reason": "Duplicate request."
    }

    response = client.post(
        "/refunds/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == "Refund request already exists."

def test_refund_only_completed_orders(
    client,
    customer_headers,
    paid_order,
):

    payload = {
        "order_id": paid_order["id"],
        "reason": "Changed my mind."
    }

    response = client.post(
        "/refunds/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == "Only completed orders can be refunded."


def test_get_refund(
    client,
    customer_headers,
    refund,
):

    response = client.get(
        f"/refunds/{refund['id']}",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_200_OK


def test_invalid_refund(
    client,
    admin_headers,
):

    response = client.get(
        f"/refunds/{uuid4()}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_refunds(
    client,
    admin_headers,
    refund,
):

    response = client.get(
        "/refunds/",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) >= 1


def test_approve_refund(
    client,
    admin_headers,
    refund,
):

    response = client.patch(
        f"/refunds/{refund['id']}/approve",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["status"] == "approved"


def test_refund_marks_payment_refunded(
    client,
    admin_headers,
    refund,
):

    client.patch(
        f"/refunds/{refund['id']}/approve",
        headers=admin_headers,
    )

    order = client.get(
        f"/orders/{refund['order_id']}/payments",
        headers=admin_headers,
    ).json()

    assert order[0]["payment_status"] == "refunded"        

def test_refund_marks_order_refunded(
    client,
    admin_headers,
    refund,
):

    client.patch(
        f"/refunds/{refund['id']}/approve",
        headers=admin_headers,
    )

    order = client.get(
        f"/orders/{refund['order_id']}",
        headers=admin_headers,
    ).json()

    assert order["status"] == "refunded"

def test_already_approved_refund(
    client,
    admin_headers,
    refund,
):

    client.patch(
        f"/refunds/{refund['id']}/approve",
        headers=admin_headers,
    )

    response = client.patch(
        f"/refunds/{refund['id']}/approve",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_reject_refund(
    client,
    admin_headers,
    refund,
):

    response = client.patch(
        f"/refunds/{refund['id']}/reject",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["status"] == "rejected"

def test_already_rejected_refund(
    client,
    admin_headers,
    refund,
):

    client.patch(
        f"/refunds/{refund['id']}/reject",
        headers=admin_headers,
    )

    response = client.patch(
        f"/refunds/{refund['id']}/reject",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

