from fastapi import APIRouter


airflow_router = APIRouter()


@airflow_router.post("/")
async def stub():
    return {}
