from datetime import datetime, UTC

from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.base import Base
from src.role.models import Role  # noqa


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    hash_password: Mapped[str] = mapped_column(String(255), nullable=False)
    reset_password_token: Mapped[str] = mapped_column(String(128), unique=True, nullable=True)
    reset_password_sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), unique=False, nullable=True, default=datetime.now(UTC))

    sign_in_count: Mapped[int] = mapped_column(Integer, unique=False, nullable=True, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False, default=True)

    last_sign_in_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), unique=False, nullable=True, default=datetime.now(UTC))
    last_sign_in_ip: Mapped[str] = mapped_column(String(32), unique=False, nullable=True)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(UTC))

    role = relationship("Role", back_populates="users", uselist=False)
    accounts = relationship("Account", back_populates="user")
    categories = relationship("Category", back_populates="user")