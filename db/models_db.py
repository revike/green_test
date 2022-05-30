from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, DateTime

from db.base import metadata

inbox = Table(
    'inbox', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, unique=True),
    Column('code', String),
    Column('name', String),
    Column('created_at', DateTime, default=datetime.utcnow),
)
