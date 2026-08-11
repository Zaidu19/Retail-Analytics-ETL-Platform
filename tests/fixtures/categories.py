import pytest

from fastapi import status


@pytest.fixture
def category(client, admin_headers):
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

    return response.json()