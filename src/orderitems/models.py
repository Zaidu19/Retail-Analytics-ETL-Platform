from uuid import UUID
from sqlalchemy import Numeric,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship

from decimal import Decimal
from src.db.base import Base
from src.common.mixin import UUIDPrimaryKeyMixin,TimestampMixin
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.orders.models import OrderModel
    from src.products.models import ProductModel

class OrderItemModel(UUIDPrimaryKeyMixin,TimestampMixin,Base):
    __tablename__ ="order_items"

    order_id:Mapped[UUID] =mapped_column(ForeignKey("orders.id"),nullable=False)
    product_id:Mapped[UUID] =mapped_column(ForeignKey("products.id"),nullable=False)
    quantity:Mapped[int] = mapped_column(nullable=False)
    unit_price:Mapped[Decimal] = mapped_column(Numeric(12,2),nullable=False)

    order: Mapped["OrderModel"] = relationship(back_populates="order_items",)
    product: Mapped["ProductModel"] = relationship(back_populates="order_items")

