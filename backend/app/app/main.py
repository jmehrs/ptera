from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core import settings

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(api_router, prefix=settings.API_V1_STR)
