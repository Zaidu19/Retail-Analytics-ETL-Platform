import random

from sqlalchemy import select
from fastapi import HTTPException

from scripts.database import get_session
from scripts.utils import fake

from src.orders.models import OrderModel
from src.payments.models import PaymentModel
from src.refund.models import RefundModel

from src.refund.dtos import RefundCreateSchema
from src.refund.service import (
    create_refund,
    approve_refund,
    reject_refund,
)

from src.common.enum import (
    OrderStatus,
    PaymentStatus,
)


def seed_refunds():
    db = get_session()

    print("Seeding refunds...")

    # Make some orders eligible for refunds
    orders = db.scalars(
        select(OrderModel)
    ).all()

    for order in orders:
        if random.random() < 0.30:
            order.status = OrderStatus.completed

            payment = order.payment
            if payment:
                payment.payment_status = PaymentStatus.success

    db.commit()

    # Pick 10% of completed orders
    completed_orders = db.scalars(
        select(OrderModel).where(
            OrderModel.status == OrderStatus.completed
        )
    ).all()

    if not completed_orders:
        db.close()
        print("No completed orders found.")
        return

    refund_orders = random.sample(
        completed_orders,
        k=max(1, len(completed_orders) // 10),
    )

    # Create refund requests
    for order in refund_orders:
        try:
            create_refund(
                RefundCreateSchema(
                    order_id=order.id,
                    reason=fake.sentence(nb_words=6),
                ),
                order.customer.user,
                db,
            )
        except HTTPException:
            continue

    # Approve / Reject / Leave Pending
    refunds = db.scalars(
        select(RefundModel)
    ).all()

    for refund in refunds:
        try:
            chance = random.random()

            if chance < 0.60:
                approve_refund(refund.id, db)

            elif chance < 0.80:
                reject_refund(refund.id, db)

            # Remaining 20% stay pending

        except HTTPException:
            continue

    db.close()

    print("✅ Refunds seeded successfully.")