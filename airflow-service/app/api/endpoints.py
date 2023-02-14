from fastapi import APIRouter
import json
from app.api.utils import *

airflow_router = APIRouter()


@airflow_router.post("/search")
async def airflow_search():
    nonblock(get_provider_b_data)
    nonblock(get_provider_a_data)

    provider_a_data = json.load(open("provider_a_results.json", "r"))
    provider_b_data = json.load(open("provider_b_results.json", "r"))

    if provider_a_data["search_id"]:
        return {"search_id": provider_a_data["search_id"]}

    elif provider_b_data["search_id"]:
        return {"search_id": provider_b_data["search_id"]}

    return {"search_id": None}


@airflow_router.get("/results/{search_id}/{currency}")
async def airflow_results(search_id: str, currency: str):
    nonblock(get_provider_b_data)
    nonblock(get_provider_a_data)

    provider_a_data = json.load(open("provider_a_results.json", "r"))
    provider_b_data = json.load(open("provider_b_results.json", "r"))

    provider_a_data_by_search_id = get_data_by_search_id_in_providers(
        provider_a_data, search_id, currency
    )

    if provider_a_data_by_search_id:
        return provider_a_data_by_search_id

    else:
        provider_b_data_by_search_id = get_data_by_search_id_in_providers(
            provider_b_data, search_id, currency
        )
        if provider_b_data_by_search_id:
            return provider_b_data_by_search_id

        return {"detail": "Not found"}
