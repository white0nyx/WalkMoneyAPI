import sqlalchemy as sa
from sqlalchemy import Integer, String, DECIMAL, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.account_type.models import AccountType  # noqa
from src.common.base import Base
from src.currency.models import Currency  # noqa
from src.user.models import User  # noqa


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), nullable=False)
    currency_id: Mapped[int] = mapped_column(sa.ForeignKey("currencies.id"), nullable=True)
    type_id: Mapped[int] = mapped_column(sa.ForeignKey("account_types.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    balance: Mapped[DECIMAL] = mapped_column(DECIMAL(15, 2), nullable=False, default=0)
    icon_url: Mapped[str] = mapped_column(String(255), nullable=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="accounts", uselist=False)
    currency = relationship("Currency", back_populates="accounts", uselist=False)
    account_type = relationship("AccountType", back_populates="accounts", uselist=False)

    transactions = relationship(
        "Transaction",
        foreign_keys="[Transaction.account_id]",
        back_populates="account",
        cascade="all, delete-orphan",
    )

    received_transfers = relationship(
        "Transaction",
        foreign_keys="[Transaction.transfer_to_account_id]",
        back_populates="transfer_to_account",
    )