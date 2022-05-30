import os
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from core.config import PHOTO_TMP
from endpoints.depends import get_inbox_repository
# from models.inbox import Inbox
from repositories.inbox import InboxRepository

router = APIRouter()


# @router.get('/', response_model=List[Inbox])
# async def read_inbox(
#         limit=100, skip=0,
#         inbox: InboxRepository = Depends(get_inbox_repository), ):
#     return await inbox.get_all(limit, skip)


@router.post('/')
async def create_inbox(
        files: List[UploadFile] = File(description='Upload files.jpg',
                                       max_items=15),
        inbox: InboxRepository = Depends(get_inbox_repository)):
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
