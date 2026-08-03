
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.common.mixin import UUIDPrimaryKeyMixin, TimestampMixin
from src.common.enum import UserRole


class UserModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(100),unique=True, nullable=False,index=True,)

    email: Mapped[str] = mapped_column(String(255),unique=True,nullable=False,index=True,)

    password_hash: Mapped[str] = mapped_column(String(255),nullable=False,)

    role: Mapped[UserRole] = mapped_column(Enum(UserRole),nullable=False,)

    is_active: Mapped[bool] = mapped_column(Boolean,default=True,nullable=False,)