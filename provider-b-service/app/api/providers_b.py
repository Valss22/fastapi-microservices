from fastapi import APIRouter
import json
import asyncio

providers_b = APIRouter()


@providers_b.post("/search")
async def provider_b_search():
    data = json.load(open("app/api/response_b.json", "r"))
    # await asyncio.sleep(60)
    return data
