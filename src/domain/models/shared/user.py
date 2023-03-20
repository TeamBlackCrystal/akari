from __future__ import annotations

from datetime import datetime
import uuid
from sqlalchemy import Boolean, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(String, default=str(uuid.uuid4()), primary_key=True)
    misskey_id: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(Date, default=datetime.utcnow)
    strike: Mapped[list[Strike]] = relationship()
    reminder: Mapped[list[Reminder]] = relationship()


class Strike(Base):
    __tablename__ = 'strikes'

    id: Mapped[str] = mapped_column(String, default=str(uuid.uuid4()), primary_key=True)
    user: Mapped[User] = mapped_column(ForeignKey('users.id'))
    reason: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(Date, default=datetime.utcnow)


class Reminder(Base):
    __tablename__ = 'reminders'

    id: Mapped[str] = mapped_column(String, default=str(uuid.uuid4()), primary_key=True)
    user: Mapped[User] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(String)
    note_id: Mapped[str] = mapped_column(String, unique=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(Date, default=datetime.utcnow)
