from fastapi import FastAPI
from app.api.endpoints import provider_b_router

app = FastAPI(
    openapi_url="/api/v1/providers_b/openapi.json", docs_url="/api/v1/providers_b/docs"
)

app.include_router(
    provider_b_router, prefix="/api/v1/providers_b", tags=["providers_b"]
)
