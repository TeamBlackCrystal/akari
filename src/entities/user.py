from __future__ import annotations

from datetime import datetime
import uuid
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from packages.shared.db import Base


class User(Base):
    __tablename__ = 'users'
    misskey_id: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())

    strikes: Mapped[list['Strike']] = relationship(back_populates='user')
    reminders: Mapped[list['Reminder']] = relationship(back_populates='user')


class Strike(Base):
    __tablename__ = 'strikes'

    id: Mapped[str] = mapped_column(default=str(uuid.uuid4()), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.misskey_id'))
    user: Mapped[User] = relationship(back_populates='strikes')
    reason: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())


class Reminder(Base):
    __tablename__ = 'reminders'

    id: Mapped[str] = mapped_column(default=str(uuid.uuid4()), primary_key=True)

    user_id: Mapped[str] = mapped_column(ForeignKey('users.misskey_id'))
    user: Mapped['User'] = relationship(back_populates='reminders')

    title: Mapped[str] = mapped_column()
    note_id: Mapped[str] = mapped_column(unique=True)
    is_done: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
