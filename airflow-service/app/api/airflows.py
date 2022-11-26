import os
from fastapi import APIRouter
import httpx
import xmltodict

airflows = APIRouter()


def convert_currency(from_currency: str, to_currency: str, amount: float) -> float:
    if from_currency == to_currency:
        return amount
    url = "https://www.nationalbank.kz/rss/get_rates.cfm?fdate=26.10.2021"
    response_xml = httpx.get(url)
    response_dict = xmltodict.parse(response_xml.text)
    currency_items = response_dict["rates"]["item"]
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
                    price_item = results[i]["items"][j]["price"]
                    price_item["amount"] = convert_currency(
                        price_item["currency"], currency, price_item["amount"]
                    )
                    price_item["currency"] = currency
                return results[i]
        i += 1
    return {"detail": "not found"}
