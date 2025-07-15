from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import BaseTimeStamped


class User(BaseTimeStamped):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    hh_user_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    
    hh_token: Mapped["HeadHunterToken"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id})>"


class HeadHunterToken(BaseTimeStamped):
    __tablename__ = "head_hunter_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    token_type: Mapped[str]
    access_token: Mapped[str]
    refresh_token: Mapped[str]
    expires_in: Mapped[int]

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="hh_token")
    
    def __repr__(self):
        return (
            f"<HeadHunterToken(id={self.id}, "
            f"user_id={self.user_id})>"
        )