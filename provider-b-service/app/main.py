from fastapi import FastAPI
from app.api.providers_b import providers_b

app = FastAPI(
    openapi_url="/api/v1/providers_b/openapi.json", docs_url="/api/v1/providers_b/docs"
)

app.include_router(providers_b, prefix="/api/v1/providers_b", tags=["providers_b"])
