from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="boards")
    columns: Mapped[list["Column"]] = relationship(back_populates="board", cascade="all, delete-orphan")
