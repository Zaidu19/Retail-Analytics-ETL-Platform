from scripts.database import get_session
from scripts.utils import fake

import random

from sqlalchemy import select

from src.orders.service import create_order
from src.orders.dtos import OrderCreateSchema
from src.customers.models import CustomerModel
from src.products.models import ProductModel
from src.orders.dtos import OrderItemInputSchema
from src.common.enum import PaymentMethod


def seed_orders():
    db = get_session()

    print("Seeding orders...")

    customers = db.scalars(
        select(CustomerModel)
    ).all()

    customer_users = [customer.user for customer in customers]

    products_ids = db.scalars(
        select(ProductModel.id)
    ).all()

    for _ in range(200):
        current_user = random.choice(customer_users)

        selected_products_ids = random.sample(
            products_ids,
            k=random.randint(1, 4),
        )

        items = []

        for product_id in selected_products_ids:
            items.append(
                OrderItemInputSchema(
                    product_id=product_id,
                    quantity=random.randint(1, 3),
                )
            )

        create_order(
            OrderCreateSchema(
                payment_method=random.choice(list(PaymentMethod)),
                items=items,
            ),
            current_user,
            db,
        )

    db.close()

    print("✅ Orders seeded successfully.")   