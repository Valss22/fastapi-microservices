from fastapi import FastAPI
from app.api.providers_b import providers_b
from app.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(
    openapi_url="/api/v1/providers_b/openapi.json", docs_url="/api/v1/providers_b/docs"
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(providers_b, prefix="/api/v1/providers_b", tags=["providers_b"])
