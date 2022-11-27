import os
from fastapi import APIRouter
import httpx
import xmltodict
import json
from datetime import datetime

airflows = APIRouter()

PROVIDER_A_HOST_URL = os.environ.get("PROVIDER_A_HOST_URL")
PROVIDER_B_HOST_URL = os.environ.get("PROVIDER_B_HOST_URL")


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


@airflows.post("/search")
async def airflow_search():
    provider_a_response = httpx.post(PROVIDER_A_HOST_URL + "/search")
    provider_b_response = httpx.post(PROVIDER_B_HOST_URL + "/search")
    return provider_a_response.json()


@airflows.get("/results/{search_id}/{currency}")
async def airflow_results(search_id: str, currency: str):
    provider_a_response = httpx.post(PROVIDER_A_HOST_URL + "/search")
    results = provider_a_response.json()
    i = 0
    for data_el in results:
        for value in data_el.values():
            if value == search_id:
                for j in range(len(data_el["items"])):
                    price_item = results[i]["items"][j]["price"]
                    price_item["amount"] = convert_currency(
                        price_item["currency"], currency, price_item["amount"]
                    )
                    price_item["currency"] = currency
                sorted_items = sorted(
                    results[i]["items"],
                    key=lambda d: d["price"]["amount"],
                )
                results[i]["items"] = sorted_items
                return results[i]
        i += 1
    return {"detail": "not found"}
