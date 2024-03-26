from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.config.database import get_async_session, Model
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, TYPE_CHECKING
from fastapi import Depends
if TYPE_CHECKING:
    from src.sounds import Sound


class User(SQLAlchemyBaseUserTable[int], Model):
    username: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    is_artist: Mapped[bool] = mapped_column(Boolean, default=False)
    links: Mapped[List["Links"]] = relationship(
        back_populates="user", uselist=True
    )
    profiles: Mapped[List["Profiles"]] = relationship(
        back_populates="user", uselist=True
    )
    sounds: Mapped[List["Sound"]] = relationship(
        back_populates="authors", uselist=True
    )


class Profiles(Model):
    __tablename__ = "profiles"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    image_urls: Mapped[str] = mapped_column(String, unique=True)
    user: Mapped["User"] = relationship(
        back_populates="profiles", uselist=True
    )


class Links(Model):
    __tablename__ = "links"
    link: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(
        back_populates="links", uselist=True
    )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
