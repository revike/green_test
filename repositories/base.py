from databases import Database


class BaseRepository:
    """Base Repository"""

    def __init__(self, database: Database):
        self.database = database
