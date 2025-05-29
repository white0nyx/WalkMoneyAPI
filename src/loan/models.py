from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import Integer, DECIMAL, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.account.models import Account  # noqa
from src.common.base import Base


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(15, 2), nullable=False)
    from_account_id: Mapped[int] = mapped_column(sa.ForeignKey("accounts.id"), nullable=False)
    loan_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    repayment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    loan_status: Mapped[str] = mapped_column(String(50), default='active')

    from_account = relationship("Account", back_populates="loans")
