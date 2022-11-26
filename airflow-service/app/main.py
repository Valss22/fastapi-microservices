from fastapi import FastAPI
from app.api.airflows import airflows
from app.db import metadata, database, engine
from app.api.airflows import download_currency_rates

metadata.create_all(engine)

app = FastAPI(
    openapi_url="/api/v1/airflows/openapi.json", docs_url="/api/v1/airflows/docs"
)


@app.on_event("startup")
async def startup():
    download_currency_rates()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(airflows, prefix="/api/v1/airflows", tags=["airflows"])
