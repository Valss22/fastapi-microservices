from fastapi import FastAPI
from app.endpoints import provider_a_router
from app.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(provider_a_router, prefix="/api/v1/provider_a", tags=["provider_a"])
