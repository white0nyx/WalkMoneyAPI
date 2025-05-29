from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.base import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)

    users = relationship("User", back_populates="role", uselist=False)
