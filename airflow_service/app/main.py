from fastapi import FastAPI
from app.endpoints import airflow_router
from app.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(airflow_router, prefix="/api/v1/airflow", tags=["airflow"])
