from fastapi import status


def test_analytics_ping(client):

    response = client.get("/analytics/ping")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "msg": "Analytics module is working"
    }

def test_dashboard(
    client,
    admin_headers,
):

    response = client.get(
        "/analytics/dashboard",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert "total_customers" in body
    assert "total_products" in body
    assert "total_orders" in body
    assert "completed_orders" in body
    assert "refunded_orders" in body

def test_monthly_sales(
    client,
    admin_headers,
):

    response = client.get(
        "/analytics/monthly-sales",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response.json(), list)

def test_top_products(
    client,
    admin_headers,
):

    response = client.get(
        "/analytics/top-products",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response.json(), list)

def test_top_products_revenue(
    client,
    admin_headers,
):

    response = client.get(
        "/analytics/top-products-revenue",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

def test_top_customers(
    client,
    admin_headers,
):

    response = client.get(
        "/analytics/top-customers",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK


def test_top_categories(
    client,
    admin_headers,
):

    response = client.get(
        "/analytics/top-categories",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK


def test_profit_analytics(
    client,
    admin_headers,
):

    response = client.get(
        "/analytics/profit-analytics",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

def test_refund_analytics(
    client,
    admin_headers,
):

    response = client.get(
        "/analytics/refund-analytics",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert "total_refunds" in body
    assert "refund_amounts" in body

def test_low_stock_products(
    client,
    inventory_manager_headers,
):

    response = client.get(
        "/analytics/low-stock-products",
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_200_OK


def test_out_of_stock_products(
    client,
    inventory_manager_headers,
):

    response = client.get(
        "/analytics/out-of-stock-products",
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_200_OK


def test_inventory_value(
    client,
    inventory_manager_headers,
):

    response = client.get(
        "/analytics/inventory-value",
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    assert "inventory_value" in response.json()


def test_inventory_movement(
    client,
    inventory_manager_headers,
):

    response = client.get(
        "/analytics/inventory-movement",
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert "sale" in body
    assert "restock" in body
    assert "return_" in body


def test_customer_cannot_access_monthly_sales(
    client,
    customer_headers,
):

    response = client.get(
        "/analytics/monthly-sales",
        headers=customer_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_inventory_manager_cannot_access_top_customers(
    client,
    inventory_manager_headers,
):

    response = client.get(
        "/analytics/top-customers",
        headers=inventory_manager_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_business_analyst_cannot_access_inventory_value(
    client,
    business_analyst_headers,
):

    response = client.get(
        "/analytics/inventory-value",
        headers=business_analyst_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN                                            
            
