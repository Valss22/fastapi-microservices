from fastapi import FastAPI
from app.api.providers_a import providers_a

app = FastAPI(
    openapi_url="/api/v1/providers_a/open_api.json", docs_url="/api/v1/providers_a/docs"
)


app.include_router(providers_a, prefix="/api/v1/providers_a", tags=["providers_a"])
