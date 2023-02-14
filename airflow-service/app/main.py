from fastapi import FastAPI
from app.api.endpoints import airflow_router, download_currency_rates


app = FastAPI(
    openapi_url="/api/v1/airflows/openapi.json", docs_url="/api/v1/airflows/docs"
)


@app.on_event("startup")
async def startup():
    download_currency_rates()


# @app.on_event("startup")
# def downloads_currency_rates_every_day():
#     import schedule

#     schedule.every().day.at("12:00").do(download_currency_rates)

#     while True:
#         schedule.run_pending()


app.include_router(airflow_router, prefix="/api/v1/airflows", tags=["airflows"])
