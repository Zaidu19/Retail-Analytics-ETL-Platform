import uuid
from sqlalchemy import String,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship

from src.db.base import Base
from src.common.mixin import TimestampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.products.models import ProductModel

class CategoryModel(TimestampMixin,Base):
    __tablename__ = "categories"

    id :Mapped[uuid.UUID] = mapped_column(primary_key=True,default=uuid.uuid4,)
    name:Mapped[str] = mapped_column(String(100),unique=True,nullable=False,index=True,)
    description:Mapped[str | None]=mapped_column(Text,nullable=True)

    products : Mapped[list["ProductModel"]] = relationship(back_populates="category",)