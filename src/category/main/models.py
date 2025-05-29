from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.base import Base
from src.subcategory.models import Subcategory  # noqa: F401

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    icon_url: Mapped[str] = mapped_column(String(255), nullable=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    subcategories = relationship("Subcategory", back_populates="category")
    transactions = relationship("Transaction", back_populates="category")
    user = relationship("User", back_populates="categories", uselist=False)
