from fastapi import APIRouter
import json
import asyncio

providers_a = APIRouter()


@providers_a.post("/search")
async def provider_a_search():
    data = json.load(open("app/api/response_a.json", "r"))
    await asyncio.sleep(1)
    return data
