import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean,Date,String
from sqlalchemy.orm import Mapped,mapped_column,relationship

from src.common.mixin import UUIDPrimaryKeyMixin,TimestampMixin
from src.db.base import Base


class CustomerModel(UUIDPrimaryKeyMixin,TimestampMixin,Base):
    __tablename__="customers"

    full_name: Mapped[str]=mapped_column(
        String(255),
        nullable=False,
    )

    email : Mapped[str]= mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    phone_number : Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    Country :Mapped[str]=mapped_column(
        String(100),
        nullable=False,
    )

    city :Mapped[str]=mapped_column(
        String(100),
        nullable=False,
    )

    signup_date :Mapped[date]=mapped_column(
        Date,
        nullable=False,
    )

    is_active:Mapped[Boolean]=mapped_column(
        Boolean,
        default=True,
        nullable= False,
    )
    
