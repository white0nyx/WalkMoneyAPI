import sqlalchemy as sa

from datetime import datetime, UTC
from sqlalchemy import Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.base import Base
from src.role.models import Role


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", "deleted_at", name="uix_email_deleted_at"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(512), unique=False, nullable=False)
    name: Mapped[str] = mapped_column(String(512), unique=False, nullable=True)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("roles.id"), unique=False, nullable=True)

    password: Mapped[str] = mapped_column(String(512), unique=False, nullable=False)
    reset_password_token: Mapped[str] = mapped_column(String(512), unique=True, nullable=True)
    reset_password_sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), unique=False, nullable=True, default=datetime.now(UTC))

    sign_in_count: Mapped[int] = mapped_column(sa.Integer, unique=False, nullable=True, default=0)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, unique=False, nullable=False, default=True)

    last_sign_in_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), unique=False, nullable=True, default=datetime.now(UTC))
    last_sign_in_ip: Mapped[str] = mapped_column(String(512), unique=False, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), unique=False, nullable=False, default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), unique=False, nullable=False, default=datetime.now(UTC))
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), unique=False, nullable=True, default=None)

    role = relationship("Role", back_populates="user", uselist=False)
