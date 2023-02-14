import os
import json
import httpx
import xmltodict
import asyncio
from datetime import datetime

client = httpx.AsyncClient()

PROVIDER_A_HOST_URL = os.environ.get("PROVIDER_A_HOST_URL")
PROVIDER_B_HOST_URL = os.environ.get("PROVIDER_B_HOST_URL")


def nonblock(task, *args):
    loop = asyncio.get_event_loop()
    loop.create_task(task(*args))


def download_currency_rates():
    print("download_currency_rates")
    current_day = datetime.now().strftime("%d.%m.%Y")
    url = f"https://www.nationalbank.kz/rss/get_rates.cfm?fdate={current_day}"
    response_xml = httpx.get(url)
    response_dict = xmltodict.parse(response_xml.text)

    with open("currency_rates.json", "w") as file:
        json.dump(response_dict, file)

    return response_dict


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


def get_data_by_search_id_in_providers(provider, search_id, currency):
    for value in provider.values():
        if value == search_id:
            for j in range(len(provider["items"])):
                price_item = provider["items"][j]["price"]
                price_item["amount"] = convert_currency(
                    price_item["currency"], currency, price_item["amount"]
                )
                price_item["currency"] = currency
            sorted_items = sorted(
                provider["items"],
                key=lambda d: d["price"]["amount"],
            )
            provider["items"] = sorted_items
            return provider
    return None
