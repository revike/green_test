import uvicorn
from fastapi import FastAPI

from db.base import database
from endpoints import inbox

app = FastAPI(title='GreenAtom Test')
app.include_router(inbox.router, prefix='/frames', tags=['inbox'])


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run('main:app', port=8002, host='0.0.0.0', reload=True)
