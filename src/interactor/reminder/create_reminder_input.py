from __future__ import annotations

from typing import TypedDict



class IReminderCreateInputData(TypedDict):
    user_id: str
    title: str
    note_id: str
