from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.infrastructure.database.base import BaseTimeStamped


class User(BaseTimeStamped):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    hh_user_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    
    hh_token: Mapped["HeadHunterToken"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    
    refresh_token: Mapped[list["UserRefreshToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id})>"


class UserRefreshToken(BaseTimeStamped):
    __tablename__ = "user_refresh_tokens"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="refresh_token")

    is_blacklisted: Mapped[bool] = mapped_column(default=False)
    
    def __repr__(self):
        return (
            f"<UserRefreshToken(id={self.id}, "
            f"user_id={self.user_id})>"
        )


class HeadHunterToken(BaseTimeStamped):
    __tablename__ = "head_hunter_tokens"
    
    id: Mapped[int] = mapped_column(primary_key=True)

    access_token: Mapped[str] = mapped_column(String(255))
    token_type: Mapped[str] = mapped_column(String(50))
    expires_in: Mapped[int]
    refresh_token: Mapped[str] = mapped_column(String(255))

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="hh_token")
    
    def __repr__(self):
        return (
            f"<HeadHunterToken(id={self.id}, "
            f"user_id={self.user_id})>"
        )