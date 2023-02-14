from fastapi import APIRouter
import json
import asyncio
from app.api.schemas import Item
from typing import Optional

provider_a_router = APIRouter()


@provider_a_router.post("/search")
async def provider_a_search(item: Optional[Item] = None):
    data = json.load(open("app/api/response_a.json", "r"))

    if item:
        data["items"].append(item.dict())
        with open("app/api/response_a.json", "w") as file:
            json.dump(data, file)
<<<<<<< HEAD:provider-a-service/app/api/endpoints.py

    await asyncio.sleep(1)
=======
    await asyncio.sleep(30)
>>>>>>> ba91c5a160ae04ff370c7412f876d5e12fefbae5:provider-a-service/app/api/providers_a.py
    return data
