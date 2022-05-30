from .models_db import inbox
from db.base import metadata, engine

metadata.create_all(bind=engine)
