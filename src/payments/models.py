from uuid import UUID
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey,Enum,func,DateTime,Numeric

from src.db.base import Base
from src.common.mixin import UUIDPrimaryKeyMixin,TimestampMixin
from src.common.enum import PaymentMethod,PaymentStatus
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.orders.models import OrderModel
class PaymentModel(UUIDPrimaryKeyMixin,TimestampMixin,Base):
    __tablename__ = "payments"
      
    order_id:Mapped[UUID] = mapped_column(ForeignKey("orders.id"),nullable=False)
    amount:Mapped[Decimal] = mapped_column(Numeric(12,2),nullable=False)
    payment_method:Mapped[PaymentMethod]=mapped_column(Enum(PaymentMethod),nullable=False)
    payment_status:Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus),default=PaymentStatus.pending,nullable=False)
    paid_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)

    order:Mapped["OrderModel"]=relationship(back_populates="payments")