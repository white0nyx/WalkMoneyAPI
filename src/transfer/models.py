from datetime import datetime, UTC

import sqlalchemy as sa
from sqlalchemy import Integer, DECIMAL, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.account.models import Account  # noqa
from src.common.base import Base


class Transfer(Base):
    __tablename__ = "transfers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    from_account_id: Mapped[int] = mapped_column(sa.ForeignKey("accounts.id"), nullable=False)
    to_account_id: Mapped[int] = mapped_column(sa.ForeignKey("accounts.id"), nullable=False)
    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(15, 2), nullable=False)
    transfer_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(UTC))
    description: Mapped[str] = mapped_column(Text, nullable=True)

    from_account = relationship("Account", foreign_keys=[from_account_id], backref="outgoing_transfers")
    to_account = relationship("Account", foreign_keys=[to_account_id], backref="incoming_transfers")
