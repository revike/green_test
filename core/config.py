from starlette.config import Config

config = Config('.env')

DATABASE_URL = config('DATABASE_URL', cast=str, default='')

ACCESS_KEY_MIN_IO = config('ACCESS_KEY_MIN_IO', cast=str, default='')
SECRET_KEY_MIN_IO = config('SECRET_KEY_MIN_IO', cast=str, default='')
SERVER_MIN_IO = config('SERVER_MIN_IO', cast=str, default='')
PORT_MIN_IO = config('PORT_MIN_IO', cast=str, default='')

PHOTO_TMP = config('PHOTO_TMP', cast=str, default='')
