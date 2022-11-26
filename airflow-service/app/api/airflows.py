import os
from fastapi import APIRouter
import httpx

airflows = APIRouter()


@airflows.post("/search")
async def airflow_search():
    provider_a_response = httpx.post(os.environ.get("PROVIDER_A_HOST_URL") + "/search")
    provider_b_response = httpx.post(os.environ.get("PROVIDER_B_HOST_URL") + "/search")
    return provider_a_response.json()


@airflows.get("/results/{search_id}/{currency}")
async def airflow_results(search_id: str, currency: str):
    provider_a_response = httpx.post(os.environ.get("PROVIDER_A_HOST_URL") + "/search")
    results = provider_a_response.json()
    i = 0
    for data_el in results:
        for value in data_el.values():
            if value == search_id:
                for j in range(len(data_el["items"])):
                    results[i]["items"][j]["price"]["currency"] = currency
                return results[i]
        i += 1
    return {"detail": "not found"}
