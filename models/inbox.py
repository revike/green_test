from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Inbox(BaseModel):
    """Model Inbox"""
    id: Optional[str] = None
    code: str
    name: str
    created_at: datetime
