from fastapi import FastAPI
from app.api.airflows import airflows
from app.api.airflows import download_currency_rates


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


app.include_router(airflows, prefix="/api/v1/airflows", tags=["airflows"])
