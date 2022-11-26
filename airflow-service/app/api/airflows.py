from fastapi import APIRouter

airflows = APIRouter()


@airflows.post("/search")
async def airflow_search():
    return {"detail": "Airflow search"}
