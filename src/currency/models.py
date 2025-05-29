from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.base import Base


class Currency(Base):
    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[str] = mapped_column(String(10), nullable=False)
    icon_url: Mapped[str] = mapped_column(String(255), nullable=True)

    accounts = relationship("Account", back_populates="currency")
