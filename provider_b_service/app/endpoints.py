from fastapi import APIRouter


provider_b_router = APIRouter()


@provider_b_router.post("/")
async def stub():
    return {}
