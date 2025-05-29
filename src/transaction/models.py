from datetime import datetime, UTC

import sqlalchemy as sa
from sqlalchemy import Integer, String, DECIMAL, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.account.models import Account  # noqa
from src.category.models import Category  # noqa
from src.common.base import Base
from src.subcategory.models import Subcategory  # noqa


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    account_id: Mapped[int] = mapped_column(sa.ForeignKey("accounts.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(sa.ForeignKey("categories.id"), nullable=True)
    subcategory_id: Mapped[int] = mapped_column(sa.ForeignKey("subcategories.id"), nullable=True)
    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(15, 2), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(50), nullable=True)
    transaction_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(UTC))
    description: Mapped[str] = mapped_column(Text, nullable=True)

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions", uselist=False)
    subcategory = relationship("Subcategory", back_populates="transactions", uselist=False)
