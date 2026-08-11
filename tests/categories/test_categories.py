from uuid import uuid4

from fastapi import status

def test_create_category(client, admin_headers):

    payload = {
        "name": "Electronics",
        "description": "Electronic devices such as phones, laptops, televisions and accessories."
    }

    response = client.post(
        "/categories/",
        json=payload,
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()

    assert body["name"] == payload["name"]

def test_duplicate_category(
    client,
    admin_headers,
    category,
):

    payload = {
        "name": category["name"],
        "description": "Electronic devices such as phones, laptops, televisions and accessories."
    }

    response = client.post(
        "/categories/",
        json=payload,
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Category with this name already exists."

def test_get_all_categories(
    client,
    customer_headers,
    category,
):

    response = client.get(
        "/categories/",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    categories = response.json()

    assert len(categories) >= 1

def test_get_category_by_id(
    client,
    customer_headers,
    category,
):

    response = client.get(
        f"/categories/{category['id']}",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["id"] == category["id"]

def test_get_invalid_category(
    client,
    customer_headers,
):

    response = client.get(
        f"/categories/{uuid4()}",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_category(
    client,
    inventory_manager_headers,
    category,
):

    payload = {
        "name": "Updated Electronics",
        "description": "Updated category containing electronic products, accessories and smart devices."
    }

    response = client.put(
        f"/categories/{category['id']}",
        json=payload,
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["name"] == "Updated Electronics"

def test_delete_category(
    client,
    admin_headers,
    category,
):

    response = client.delete(
        f"/categories/{category['id']}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_invalid_category(
    client,
    admin_headers,
):

    response = client.delete(
        f"/categories/{uuid4()}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_customer_cannot_create_category(
    client,
    customer_headers,
):

    payload = {
        "name": "Electronics",
        "description": "Electronic devices such as phones, laptops, televisions and accessories."
    }

    response = client.post(
        "/categories/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert response.json()["detail"] == "You do not have permission to perform this action."

def test_inventory_manager_can_update_category(
    client,
    inventory_manager_headers,
    category,
):

    payload = {
        "name": "Updated Electronics",
        "description": "Updated category containing electronic products, accessories and smart devices."
    }

    response = client.put(
        f"/categories/{category['id']}",
        json=payload,
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_200_OK                                
