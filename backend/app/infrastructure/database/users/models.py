from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import AbstractTokenModel, BaseTimeStamped


class User(BaseTimeStamped):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    hh_user_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    
    hh_token: Mapped["HeadHunterToken"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    
    token: Mapped["UserToken"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id})>"


class UserToken(AbstractTokenModel):
    __tablename__ = "user_tokens"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="token")
    
    def __repr__(self):
        return (
            f"<UserToken(id={self.id}, "
            f"user_id={self.user_id})>"
        )


class HeadHunterToken(AbstractTokenModel):
    __tablename__ = "head_hunter_tokens"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="hh_token")
    
    def __repr__(self):
        return (
            f"<HeadHunterToken(id={self.id}, "
            f"user_id={self.user_id})>"
        )