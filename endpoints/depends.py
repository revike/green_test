from db.base import database
from repositories.inbox import InboxRepository


def get_inbox_repository() -> InboxRepository:
    return InboxRepository(database)