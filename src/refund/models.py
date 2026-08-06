
from uuid import UUID

from decimal import Decimal
from sqlalchemy.orm import Mapped,mapped_column,relationship
from typing import TYPE_CHECKING
from sqlalchemy import Text,DateTime,ForeignKey,Enum,Numeric
from datetime import datetime,timezone
from src.db.base import Base
from src.common.enum import RefundStatus
from src.common.mixin import UUIDPrimaryKeyMixin,TimestampMixin
if TYPE_CHECKING:
    from src.orders.models import OrderModel
class RefundModel(UUIDPrimaryKeyMixin,TimestampMixin,Base):
    __tablename__ = "refunds"

    order_id:Mapped[UUID] = mapped_column(ForeignKey("orders.id"),unique=True,nullable=False)
    amount:Mapped[Decimal] = mapped_column(Numeric(12,2),nullable=False)
    reason :Mapped[str] = mapped_column(Text,nullable= False)
    status:Mapped[RefundStatus] = mapped_column(Enum(RefundStatus),default=RefundStatus.pending,nullable= False)
    requested_at:Mapped[datetime]= mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)
    processed_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)

    order: Mapped["OrderModel"] = relationship(back_populates="refund")




