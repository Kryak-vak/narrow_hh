from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, BaseTimeStamped


class User(BaseTimeStamped):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    
    auth_profile: Mapped["TelegramProfile"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    
    token: Mapped["UserToken"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id})>"


class TelegramProfile(BaseTimeStamped):
    __tablename__ = "telegram_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="auth_profile")

    def __repr__(self):
        return f"<TelegramProfile(id={self.id}, telegram_id={self.telegram_id})>"


class UserToken(Base):
    __tablename__ = "user_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    token_type: Mapped[str]
    access_token: Mapped[str]
    refresh_token: Mapped[str]
    expires_in: Mapped[int]

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="token")
    
    def __repr__(self):
        return f"<UserToken(id={self.id}, user_id={self.user_id}, expires_in={self.expires_in})>"