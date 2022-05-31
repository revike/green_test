import io
import os
import uuid
from datetime import datetime
from core.config import PHOTO_TMP
from db import inbox
from min_io.minio_client import client
from models.inbox import Inbox
from repositories.base import BaseRepository


class InboxRepository(BaseRepository):
    """Methods for Inbox Repository"""

    async def create(self, file_name_list):
        """Create Inbox"""
        values = []
        bucket_name = datetime.utcnow().date().strftime('%Y%m%d')
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
        code = f'{uuid.uuid4()}'
        for file_name in file_name_list:
            file = f'{PHOTO_TMP}/{file_name}'
            with open(file, 'rb') as obj:
                client.put_object(bucket_name=bucket_name,
                                  object_name=file_name,
                                  data=io.BytesIO(obj.read()),
                                  length=-1,
                                  part_size=104857600)
            in_box = Inbox(code=code, name=file_name,
                           created_at=datetime.utcnow())
            value = {**in_box.dict()}
            value.pop('id', None)
            query = inbox.insert().values(**value)
            in_box.id = await self.database.execute(query=query)
            values.append(in_box)
            os.remove(file)
        return values

    async def get_data(self, code, limit=None, skip=None):
        """Get list data for database"""
        query = inbox.select().limit(limit).offset(skip)
        if code:
            query = query.filter_by(code=code)
        return await self.database.fetch_all(query=query)

    async def delete(self, code):
        """Delete list img for database and min.io"""
        query = inbox.delete().where(inbox.c.code == code)
        return await self.database.fetch_all(query=query)
