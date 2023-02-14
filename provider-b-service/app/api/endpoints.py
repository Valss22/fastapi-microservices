from fastapi import APIRouter
import json
import asyncio
from app.api.schemas import Item
from typing import Optional

providers_b = APIRouter()


@providers_b.post("/search")
async def provider_a_search(item: Optional[Item] = None):
    data = json.load(open("app/api/response_b.json", "r"))

    if item:
        data["items"].append(item.dict())
        with open("app/api/response_b.json", "w") as file:
            json.dump(data, file)

    await asyncio.sleep(2)
    return data
