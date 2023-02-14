from fastapi import FastAPI
from app.api.endpoints import provider_a_router

app = FastAPI(
    openapi_url="/api/v1/providers_a/open_api.json", docs_url="/api/v1/providers_a/docs"
)


app.include_router(
    provider_a_router, prefix="/api/v1/providers_a", tags=["providers_a"]
)
