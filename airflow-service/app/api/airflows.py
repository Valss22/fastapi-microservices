from fastapi import APIRouter


import httpx

airflows = APIRouter()


@airflows.post("/search")
async def airflow_search():
    # provider_a_response = await httpx.get("http://provider-a:8000/api/v1/search")
    # provider_b_response = await httpx.get("http://provider-b:8000/api/v1/search")
    # return provider_a_response.json() + provider_b_response.json()
    return {}


@airflows.get("/results/{search_id}/{currency}")
async def airflow_results(search_id: str, currency: str):
    return {"detail": "Airflow results"}
