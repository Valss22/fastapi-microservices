from fastapi import APIRouter

providers_a = APIRouter()


@providers_a.post("/search")
async def provider_a_search():

    return {"detail": "Provider A search"}
