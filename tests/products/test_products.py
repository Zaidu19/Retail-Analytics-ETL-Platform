from fastapi import status


def test_create_product(
    client,
    admin_headers,
    category,
):

    payload = {
        "name": "Samsung S25",
        "description": "Premium Samsung flagship smartphone with AI features.",
        "category_id": category["id"],
        "price": "75000.00",
        "cost": "60000.00",
        "stock_qty": 50,
    }

    response = client.post(
        "/products/",
        json=payload,
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()

    assert body["name"] == payload["name"]
    assert body["category_id"] == category["id"]

def test_duplicate_product(
    client,
    admin_headers,
    product,
):

    payload = {
        "name": product["name"],
        "description": product["description"],
        "category_id": product["category_id"],
        "price": "90000.00",
        "cost": "70000.00",
        "stock_qty": 10,
    }

    response = client.post(
        "/products/",
        json=payload,
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Product already exists."

from uuid import uuid4


def test_create_product_invalid_category(
    client,
    admin_headers,
):

    payload = {
        "name": "MacBook",
        "description": "Powerful Apple laptop for software development.",
        "category_id": str(uuid4()),
        "price": "150000.00",
        "cost": "120000.00",
        "stock_qty": 10,
    }

    response = client.post(
        "/products/",
        json=payload,
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_customer_cannot_create_product(
    client,
    customer_headers,
    category,
):

    payload = {
        "name": "Nothing Phone",
        "description": "Modern smartphone with transparent design and clean software.",
        "category_id": category["id"],
        "price": "35000.00",
        "cost": "25000.00",
        "stock_qty": 25,
    }

    response = client.post(
        "/products/",
        json=payload,
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN   


def test_get_all_products(
    client,
    customer_headers,
    product,
):

    response = client.get(
        "/products/",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    products = response.json()

    assert len(products) >= 1


def test_get_product_by_id(
    client,
    customer_headers,
    product,
):

    response = client.get(
        f"/products/{product['id']}",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["id"] == product["id"]


from uuid import uuid4

def test_get_invalid_product(
    client,
    customer_headers,
):

    response = client.get(
        f"/products/{uuid4()}",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Product not found."


def test_update_product(
    client,
    admin_headers,
    product,
):

    payload = {
        "name": "Updated iPhone",
        "description": "Updated Apple smartphone with improved battery and camera performance.",
        "price": "109999.99",
        "cost": "85000.00",
        "stock_qty": 30,
    }

    response = client.put(
        f"/products/{product['id']}",
        json=payload,
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["name"] == "Updated iPhone"
    assert body["stock_qty"] == 30


def test_update_invalid_product(
    client,
    admin_headers,
):

    payload = {
        "name": "Test Product"
    }

    response = client.put(
        f"/products/{uuid4()}",
        json=payload,
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_product_invalid_category(
    client,
    admin_headers,
    product,
):

    payload = {
        "category_id": str(uuid4())
    }

    response = client.put(
        f"/products/{product['id']}",
        json=payload,
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_duplicate_product_update(
    client,
    admin_headers,
    category,
    product,
):

    response = client.post(
        "/products/",
        json={
            "name": "Samsung S25",
            "description": "Samsung flagship smartphone with AI features and premium build quality.",
            "category_id": category["id"],
            "price": "80000.00",
            "cost": "60000.00",
            "stock_qty": 20,
        },
        headers=admin_headers,
    )

    second_product = response.json()

    response = client.put(
        f"/products/{second_product['id']}",
        json={
            "name": product["name"]
        },
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Product already exist in this category."



def test_delete_product(
    client,
    admin_headers,
    product,
):

    response = client.delete(
        f"/products/{product['id']}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_invalid_product(
    client,
    admin_headers,
):

    response = client.delete(
        f"/products/{uuid4()}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_customer_cannot_delete_product(
    client,
    customer_headers,
    product,
):

    response = client.delete(
        f"/products/{product['id']}",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN                            
        
     
        