import os
from fastapi import APIRouter
import httpx

airflows = APIRouter()


@airflows.post("/search")
async def airflow_search():
    provider_a_response = httpx.post(os.environ.get("PROVIDER_A_HOST_URL") + "/search")
    provider_b_response = httpx.post(os.environ.get("PROVIDER_B_HOST_URL") + "/search")
    return {**provider_a_response.json(), **provider_b_response.json()}


@airflows.get("/results/{search_id}/{currency}")
async def airflow_results(search_id: str, currency: str):
    return {"detail": "Airflow results"}
