from fastapi import status


def test_create_inventory_restock(
    client,
    inventory_manager_headers,
    product,
):

    payload = {
        "product_id": product["id"],
        "change_qty": 20,
        "reason": "restock",
    }

    response = client.post(
        "/inventory_logs/",
        json=payload,
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()

    assert body["reason"] == "restock"

def test_create_damage_log(
    client,
    inventory_manager_headers,
    product,
):

    payload = {
        "product_id": product["id"],
        "change_qty": 2,
        "reason": "damage",
    }

    response = client.post(
        "/inventory_logs/",
        json=payload,
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    assert response.json()["reason"] == "damage"

def test_sale_inventory_log_cannot_be_created_manually(
    client,
    inventory_manager_headers,
    product,
):

    payload = {
        "product_id": product["id"],
        "change_qty": 2,
        "reason": "sale",
    }

    response = client.post(
        "/inventory_logs/",
        json=payload,
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert (
        response.json()["detail"]
        == "Sale inventory logs are created automatically through order workflow."
    )

def test_get_inventory_log(
    client,
    inventory_manager_headers,
    inventory_log,
):

    response = client.get(
        f"/inventory_logs/{inventory_log['id']}",
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_200_OK

from uuid import uuid4


def test_invalid_inventory_log(
    client,
    inventory_manager_headers,
):

    response = client.get(
        f"/inventory_logs/{uuid4()}",
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert response.json()["detail"] == "Inventory not found."

def test_list_inventory_logs(
    client,
    inventory_manager_headers,
    inventory_log,
):

    response = client.get(
        "/inventory_logs/",
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) >= 1

def test_customer_cannot_view_inventory_logs(
    client,
    customer_headers,
):

    response = client.get(
        "/inventory_logs/",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_order_creates_sale_inventory_log(
    client,
    inventory_manager_headers,
    pending_order,
    product,
):

    response = client.get(
        f"/products/{product['id']}/inventory-logs",
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    logs = response.json()

    assert any(log["reason"] == "sale" for log in logs)


def test_refund_creates_return_inventory_log(
    client,
    inventory_manager_headers,
    refund,
    product,
    admin_headers,
):

    client.patch(
        f"/refunds/{refund['id']}/approve",
        headers=admin_headers,
    )

    response = client.get(
        f"/products/{product['id']}/inventory-logs",
        headers=inventory_manager_headers,
    )

    logs = response.json()

    assert any(log["reason"] == "return" for log in logs)

def test_adjustment_cannot_make_stock_negative(
    client,
    inventory_manager_headers,
    product,
):

    payload = {
        "product_id": product["id"],
        "change_qty": -1000,
        "reason": "adjustment",
    }

    response = client.post(
        "/inventory_logs/",
        json=payload,
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == "Adjustment would result in negative stock."

def test_inventory_adjustment_success(
    client,
    inventory_manager_headers,
    product,
):

    payload = {
        "product_id": product["id"],
        "change_qty": -2,
        "reason": "adjustment",
    }

    response = client.post(
        "/inventory_logs/",
        json=payload,
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()

    assert body["reason"] == "adjustment"
    assert body["change_qty"] == -2


def test_damage_cannot_exceed_stock(
    client,
    inventory_manager_headers,
    product,
):

    payload = {
        "product_id": product["id"],
        "change_qty": 1000,
        "reason": "damage",
    }

    response = client.post(
        "/inventory_logs/",
        json=payload,
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json()["detail"] == "Insufficient stock."
                

                