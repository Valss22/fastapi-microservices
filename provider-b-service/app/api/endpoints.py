from fastapi import APIRouter
import json
import asyncio
from app.api.schemas import Item
from typing import Optional

provider_b_router = APIRouter()


@provider_b_router.post("/search")
async def provider_a_search(item: Optional[Item] = None):
    data = json.load(open("app/api/response_b.json", "r"))

    if item:
        data["items"].append(item.dict())
        with open("app/api/response_b.json", "w") as file:
            json.dump(data, file)
<<<<<<< HEAD:provider-b-service/app/api/endpoints.py

    await asyncio.sleep(2)
=======
    await asyncio.sleep(60)
>>>>>>> ba91c5a160ae04ff370c7412f876d5e12fefbae5:provider-b-service/app/api/providers_b.py
    return data
