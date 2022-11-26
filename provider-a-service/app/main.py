from fastapi import FastAPI
from app.api.providers_a import providers_a
from app.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(
    openapi_url="/api/v1/providers_a/open_api.json", docs_url="/api/v1/providers_a/docs"
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(providers_a, prefix="/api/v1/providers_a", tags=["providers_a"])
