from fastapi import APIRouter


provider_a_router = APIRouter()


@provider_a_router.post("/")
async def stub():
    return {}
