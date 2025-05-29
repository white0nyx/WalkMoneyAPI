import sqlalchemy as sa
from sqlalchemy import Integer, DECIMAL, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.category.models import Category  # noqa
from src.common.base import Base
from src.user.models import User  # noqa


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(sa.ForeignKey("categories.id"), nullable=True)
    budget_amount: Mapped[DECIMAL] = mapped_column(DECIMAL(15, 2), nullable=False)
    start_date: Mapped[str] = mapped_column(Date, nullable=True)
    end_date: Mapped[str] = mapped_column(Date, nullable=True)

    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets", uselist=False)
