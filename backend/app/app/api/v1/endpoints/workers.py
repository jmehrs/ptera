from typing import Optional

from app.core import inspector
from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/", summary="Get worker stats", response_description="A list of all workers"
)
async def get_worker_stats(worker_name: Optional[str] = None):
    stats = await inspector.inspect_worker(worker_name)
    return stats
