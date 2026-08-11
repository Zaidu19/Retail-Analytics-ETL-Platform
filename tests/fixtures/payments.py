import pytest
from sqlalchemy import select

from src.payments.models import PaymentModel


@pytest.fixture
def payment(db, pending_order):

    payment = db.scalars(
        select(PaymentModel).where(
            PaymentModel.order_id == pending_order["id"]
        )
    ).first()

    assert payment is not None

    return payment