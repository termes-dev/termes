from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    deleted: Mapped[bool] = mapped_column(default=False)

    profile: Mapped["UserProfile"] = relationship(back_populates="user", lazy="selectin")
    credentials: Mapped["UserCredentials"] = relationship(back_populates="user", lazy="selectin")
    sessions: Mapped[list["UserSession"]] = relationship(back_populates="user", lazy="selectin")


class UserProfile(Base):
    __tablename__ = "user_profile"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str | None] = mapped_column(String(32))
    username: Mapped[str | None] = mapped_column(String(32))
    bio: Mapped[str | None] = mapped_column(String(256))

    user: Mapped[User] = relationship(back_populates="profile", lazy="joined")


class UserCredentials(Base):
    __tablename__ = "user_credentials"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    email: Mapped[str] = mapped_column(String(64))
    hashed_password: Mapped[str] = mapped_column(String(64))

    user: Mapped[User] = relationship(back_populates="credentials", lazy="joined")


class UserSession(Base):
    __tablename__ = "user_session"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    hashed_token: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    expires_on: Mapped[datetime]

    user: Mapped[User] = relationship(back_populates="sessions", lazy="joined")
