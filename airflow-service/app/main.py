from fastapi import FastAPI
from app.api.airflows import airflows
from app.api.airflows import download_currency_rates
from fastapi_utils.tasks import repeat_every

app = FastAPI(
    openapi_url="/api/v1/airflows/openapi.json", docs_url="/api/v1/airflows/docs"
)


@app.on_event("startup")
async def startup():
    download_currency_rates()


@app.on_event("startup")
@repeat_every(seconds=60)
async def downloads_currency_rates_every_day():
    from datetime import datetime

    current_hour = datetime.now().strftime("%H")
    if current_hour == "12":
        download_currency_rates()


app.include_router(airflows, prefix="/api/v1/airflows", tags=["airflows"])
