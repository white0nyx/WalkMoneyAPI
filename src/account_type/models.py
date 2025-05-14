from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.common.base import Base


class AccountType(Base):
    __tablename__ = "account_type"

    type_id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
