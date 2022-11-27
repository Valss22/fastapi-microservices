import os
from fastapi import APIRouter
import httpx
import xmltodict
import json
from datetime import datetime
import asyncio

airflows = APIRouter()

PROVIDER_A_HOST_URL = os.environ.get("PROVIDER_A_HOST_URL")
PROVIDER_B_HOST_URL = os.environ.get("PROVIDER_B_HOST_URL")


client = httpx.AsyncClient()


def nonblock(task, *args):
    loop = asyncio.get_event_loop()
    loop.create_task(task(*args))


def download_currency_rates():
    current_day = datetime.now().strftime("%d.%m.%Y")
    url = f"https://www.nationalbank.kz/rss/get_rates.cfm?fdate={current_day}"
    response_xml = httpx.get(url)
    response_dict = xmltodict.parse(response_xml.text)
    with open("currency_rates.json", "w") as file:
        json.dump(response_dict, file)
    return response_dict


def convert_currency(from_currency: str, to_currency: str, amount: float) -> float:
    if from_currency == to_currency:
        return amount
    currency_rates = json.load(open("currency_rates.json", "r"))

    currency_items = currency_rates["rates"]["item"]
    for currency_item in currency_items:
        if currency_item["title"] == to_currency:
            if from_currency == "KZT":
                return round(amount / float(currency_item["description"]), 2)
            to_currency_rate = float(currency_item["description"])
        if currency_item["title"] == from_currency:
            if to_currency == "KZT":
                return round(float(currency_item["description"]) * amount, 2)
            from_currency_rate = float(currency_item["description"])

    return round(from_currency_rate / to_currency_rate * amount, 2)


async def get_provider_a_data():
    response = await client.post(PROVIDER_A_HOST_URL + "/search")
    with open("provider_a_results.json", "w") as file:
        json.dump(response.json(), file)
    return None


async def get_provider_b_data():
    response = await client.post(PROVIDER_B_HOST_URL + "/search")
    with open("provider_b_results.json", "w") as file:
        json.dump(response.json(), file)
    return None


@airflows.post("/search")
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


@airflows.get("/results/{search_id}/{currency}")
async def airflow_results(search_id: str, currency: str):
    provider_a_data = json.load(open("provider_a_results.json", "r"))
    provider_b_data = json.load(open("provider_b_results.json", "r"))

    for value in provider_a_data.values():
        if value == search_id:
            for j in range(len(provider_a_data["items"])):
                price_item = provider_a_data["items"][j]["price"]
                price_item["amount"] = convert_currency(
                    price_item["currency"], currency, price_item["amount"]
                )
                price_item["currency"] = currency
            sorted_items = sorted(
                provider_a_data["items"],
                key=lambda d: d["price"]["amount"],
            )
            provider_a_data["items"] = sorted_items
            return provider_a_data
    return {"detail": "not found"}
