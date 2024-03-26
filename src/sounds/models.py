from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.config.database import Model, Base
from sqlalchemy import String, ForeignKey
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from src.auth import User


class Sound(Model):
    __tablename__ = "sound"
    name: Mapped[str] = mapped_column(String)
    sound_url: Mapped[str] = mapped_column(String, unique=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    authors: Mapped["User"] = relationship(
        back_populates="sounds", uselist=True
    )
    playlist: Mapped[List["Sound"]] = relationship(
        back_populates="sounds", secondary="playlist_sound"
    )


class Playlist(Model):
    __tablename__ = "playlist"
    name: Mapped[str] = mapped_column(String)
    owner: Mapped[int] = mapped_column(ForeignKey("user.id"))
    sounds: Mapped[List["Sound"]] = relationship(
        back_populates="playlist", secondary="playlist_sound"
    )


class PlaylistSound(Base):
    __tablename__ = "playlist_sound"
    playlist_id: Mapped[int] = mapped_column(
        ForeignKey("playlist.id", ondelete="CASCADE"),
        primary_key=True
    )
    sound_id: Mapped[int] = mapped_column(
        ForeignKey("sound.id", ondelete="CASCADE"),
        primary_key=True
    )
