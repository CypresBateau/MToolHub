"""GET /health — 服务健康检查。"""
from __future__ import annotations

from fastapi import APIRouter

from ..model_singleton import ModelSingleton
from ..schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health() -> HealthResponse:
    sg = ModelSingleton.get()
    return HealthResponse(
        status="ok" if sg.loaded else "loading",
        model_loaded=sg.loaded,
        checkpoint=sg.checkpoint_name,
        device=str(sg.device) if sg.device else "unknown",
        mode=sg.mode,
    )
