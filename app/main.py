from fastapi import FastAPI

from app.api.router import router as api_router


app = FastAPI(title='expense-tracker-api')
app.include_router(api_router)


@app.get('/')
async def index():
    return {'msg': 'ok'}
