from fastapi import APIRouter
import json
import asyncio
from app.api.schemas import Item
from typing import Optional

providers_a = APIRouter()


@providers_a.post("/search")
async def provider_a_search(item: Optional[Item] = None):
    data = json.load(open("app/api/response_a.json", "r"))
    if item:
        data["items"].append(item.dict())
        with open("app/api/response_a.json", "w") as file:
            json.dump(data, file)
    await asyncio.sleep(30)
    return data
