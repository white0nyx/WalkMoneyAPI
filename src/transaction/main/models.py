import enum
from datetime import datetime, UTC

import sqlalchemy as sa
from sqlalchemy import Integer, DECIMAL, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.account.main.models import Account  # noqa
from src.category.main.models import Category  # noqa
from src.common.base import Base
from src.subcategory.main.models import SubCategory  # noqa


class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False, index=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True, index=True)
    subcategory_id: Mapped[int | None] = mapped_column(ForeignKey("subcategories.id"), nullable=True, index=True)
    transfer_to_account_id: Mapped[int | None] = mapped_column(ForeignKey("accounts.id"), nullable=True, index=True)
    amount: Mapped[sa.DECIMAL] = mapped_column(DECIMAL(15, 2), nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(sa.Enum(TransactionType), nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    account = relationship("Account", foreign_keys=[account_id], back_populates="transactions")
    transfer_to_account = relationship("Account", foreign_keys=[transfer_to_account_id])
    category = relationship("Category", back_populates="transactions", uselist=False)
    subcategory = relationship("SubCategory", back_populates="transactions", uselist=False)

    __table_args__ = (
        CheckConstraint("amount != 0", name="check_amount_non_zero"),
        CheckConstraint(
            "(transaction_type = 'TRANSFER' AND transfer_to_account_id IS NOT NULL) OR "
            "(transaction_type != 'TRANSFER' AND transfer_to_account_id IS NULL)",
            name="check_transfer_account"
        ),
    )

