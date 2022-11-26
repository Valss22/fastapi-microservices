from fastapi import APIRouter

providers_b = APIRouter()


@providers_b.post("/search")
def provider_b_search():
    return {"detail": "Provider B search"}
