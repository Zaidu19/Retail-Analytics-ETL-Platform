
from datetime import datetime,timezone


from src.common.enum import PaymentStatus,OrderStatus
from src.orders.models import OrderModel
from src.payments.models import PaymentModel

def complete_payment(
    payment: PaymentModel,
    order: OrderModel,
):
    payment.payment_status = PaymentStatus.success
    payment.paid_at = datetime.now(timezone.utc)
    order.status = OrderStatus.paid

# Future automation:
# - Generate invoice
# - Send payment confirmation email
# - Notify warehouse
# - Award loyalty points


#Future:
# notify_customer_payment_failed(payment)    