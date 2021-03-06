import io
import os
import uuid
from datetime import datetime

from fastapi import HTTPException
from minio import S3Error
from starlette import status

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
        try:
            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)
        except S3Error:
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT)
        code = f'{uuid.uuid4()}'
        for file_name in file_name_list:
            file = f'{PHOTO_TMP}/{file_name}'
            try:
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
            except S3Error:
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT)
            finally:
                os.remove(file)
        return values

    async def get_data(self, code):
        """Get list data for database"""
        query = inbox.select().filter_by(code=code)
        return await self.database.fetch_all(query=query)

    async def delete(self, code, inbox_list):
        """Delete list img for database and min.io"""
        try:
            buckets_list = client.list_buckets()
        except S3Error:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT)
        for bucket in buckets_list:
            try:
                search_bucket_name = client.stat_object(
                    bucket.name, inbox_list[0].name)
                for obj in inbox_list:
                    client.remove_object(
                        search_bucket_name._bucket_name, obj.name)
                client.remove_bucket(search_bucket_name._bucket_name)
            except S3Error:
                pass

        query = inbox.delete().where(inbox.c.code == code)
        return await self.database.fetch_all(query=query)
