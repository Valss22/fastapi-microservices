from fastapi import FastAPI
<<<<<<< HEAD
from app.api.endpoints import airflow_router, download_currency_rates

=======
from app.api.airflows import airflows
from app.api.airflows import download_currency_rates
from fastapi_utils.tasks import repeat_every
>>>>>>> ba91c5a160ae04ff370c7412f876d5e12fefbae5

app = FastAPI(
    openapi_url="/api/v1/airflows/openapi.json", docs_url="/api/v1/airflows/docs"
)


@app.on_event("startup")
async def startup():
    download_currency_rates()


<<<<<<< HEAD
# @app.on_event("startup")
# def downloads_currency_rates_every_day():
#     import schedule
=======
@app.on_event("startup")
@repeat_every(seconds=60)
async def downloads_currency_rates_every_day():
    from datetime import datetime
>>>>>>> ba91c5a160ae04ff370c7412f876d5e12fefbae5

    current_hour = datetime.now().strftime("%H")
    if current_hour == "12":
        download_currency_rates()


app.include_router(airflow_router, prefix="/api/v1/airflows", tags=["airflows"])
