import uuid
from decimal import Decimal
from sqlalchemy import CheckConstraint,ForeignKey,Numeric,String,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship

from src.common.mixin import UUIDPrimaryKeyMixin,TimestampMixin
from src.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.categories.models import CategoryModel

class ProductModel(UUIDPrimaryKeyMixin,TimestampMixin,Base):
    __tablename__ ="products"

    __table_args__=(
        CheckConstraint("price >= 0",name="ck_products_price_positive"),
        CheckConstraint("cost >= 0",name="ck_products_cost_positive"),
        CheckConstraint("stock_qty >= 0", name="ck_products_stock_postive"),
    )

    name : Mapped[str]=mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description : Mapped[str |None]=mapped_column(
        Text,
        nullable= True,
    )

    category_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
    )

    price : Mapped[Decimal]=mapped_column(
        Numeric(10,2),
        nullable= False,
    )

    cost : Mapped[Decimal]=mapped_column(
        nullable=False,
        default=0,
    )

    stock_qty : Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    category : Mapped["CategoryModel"]=relationship(back_populates="products",)