from fastapi import APIRouter

from app.api.v1.endpoints import tasks, workers, canvas, result, run, schedule

api_router = APIRouter()
api_router.include_router(workers.router, prefix="/workers", tags=["workers"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(canvas.router, prefix="/canvas", tags=["canvas"])
api_router.include_router(run.router, prefix="/run", tags=["run"])
api_router.include_router(result.router, prefix="/result", tags=["result"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
