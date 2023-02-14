from datetime import datetime

from fastapi import FastAPI

from app.api.endpoints import airflow_router, download_currency_rates


app = FastAPI(
    openapi_url="/api/v1/airflows/openapi.json", docs_url="/api/v1/airflows/docs"
)


@app.on_event("startup")
async def startup():
    download_currency_rates()

    current_hour = datetime.now().strftime("%H")
    if current_hour == "12":
        download_currency_rates()


app.include_router(airflow_router, prefix="/api/v1/airflows", tags=["airflows"])
