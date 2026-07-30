
import uuid
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey,DateTime,func,Enum,Numeric
from datetime import datetime
from decimal import Decimal

from src.db.base import Base
from src.common.mixin import UUIDPrimaryKeyMixin,TimestampMixin
from src.common.enum import OrderStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.customers.models import CustomerModel
    from src.orderitems.models import OrderItemModel

class OrderModel(UUIDPrimaryKeyMixin,TimestampMixin,Base):
    __tablename__ ="orders"

    customer_id :Mapped[uuid.UUID]=mapped_column(
        ForeignKey("customers.id"),
        nullable=False
    )
    order_date :Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    status:Mapped[OrderStatus]=mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.pending,
        nullable=False
    )
    subtotal:Mapped[Decimal]=mapped_column(
        Numeric(12,2),
        nullable=False,
        default=0
    )
    discount :Mapped[Decimal]=mapped_column(
        Numeric(12,2),
        nullable=False,
        default=0
    )
    tax:Mapped[Decimal]=mapped_column(
        Numeric(12,2),
        nullable=False,
        default=0
    )
    grand_total:Mapped[Decimal]=mapped_column(
        Numeric[12,2],
        nullable=False,
        default=0
    )

    customer : Mapped["CustomerModel"] = relationship(back_populates="orders")
    order_items:Mapped[list["OrderItemModel"]] = relationship(back_populates="order",cascade="all,delete-orphan")


