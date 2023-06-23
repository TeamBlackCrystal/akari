from __future__ import annotations

from datetime import datetime
import uuid
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from packages.shared.db import Base


class NotFoundFixed(Base):
    __tablename__ = 'notfound_fixed'
    user_id: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
