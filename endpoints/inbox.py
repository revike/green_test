import os
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from starlette import status

from core.config import PHOTO_TMP
from endpoints.depends import get_inbox_repository
from repositories.inbox import InboxRepository

router = APIRouter()


@router.post('/')
async def create_inbox(
        files: List[UploadFile] = File(description='Upload files.jpg',
                                       max_items=15),
        inbox: InboxRepository = Depends(get_inbox_repository)):
    """Create inbox"""
    try:
        os.mkdir(PHOTO_TMP)
    except FileExistsError:
        old_files = os.listdir(PHOTO_TMP)
        for old_file in old_files:
            time_update = os.path.getmtime(f'{PHOTO_TMP}/{old_file}')
            time_now = datetime.timestamp(datetime.now())
            if (time_now - time_update) > 3600:  # Delete old files 1 hour
                os.remove(f'{PHOTO_TMP}/{old_file}')
    file_name_list = []
    for file in files:
        _, file_extension = os.path.splitext(f'{PHOTO_TMP}/{file.filename}')
        if file_extension not in ['.jpg', '.jpeg']:
            continue
        file_name = f'{uuid.uuid4().hex}.jpg'
        with open(f'{PHOTO_TMP}/{file_name}', 'wb') as obj:
            content = await file.read()
            obj.write(content)
            file_name_list.append(file_name)
    return await inbox.create(file_name_list=file_name_list)


@router.get('/')
async def get_inbox(code: str = '', limit: int = None, skip: int = 0,
                    inbox: InboxRepository = Depends(get_inbox_repository)):
    """Get inbox"""
    return await inbox.get_data(code, limit, skip)


@router.delete('/')
async def delete_inbox(code: str,
                       inbox: InboxRepository = Depends(get_inbox_repository)):
    """Delete inbox"""
    inbox_list = await inbox.get_data(code=code)
    if not inbox_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid page')
    await inbox.delete(code=code, inbox_list=inbox_list)
    return {'status': True}
