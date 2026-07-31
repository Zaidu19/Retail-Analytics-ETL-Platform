
from uuid import UUID
from sqlalchemy import ForeignKey,Enum
from sqlalchemy.orm import Mapped,mapped_column,relationship

from src.common.mixin import UUIDPrimaryKeyMixin,TimestampMixin
from src.db.base import Base
from src.common.enum import InventoryReason
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.products.models import ProductModel

class InventoryLogModel(UUIDPrimaryKeyMixin,TimestampMixin,Base):
    __tablename__ = "inventory_logs"

    product_id:Mapped[UUID] = mapped_column(ForeignKey("products.id"),nullable=False)
    change_qty:Mapped[int] = mapped_column(nullable=False)
    reason : Mapped[InventoryReason] = mapped_column(Enum(InventoryReason),default=InventoryReason.sale,nullable=False)

    product:Mapped["ProductModel"] = relationship(back_populates="inventory_logs")

