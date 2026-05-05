"""
routers/health.py — 健康检查端点。
"""
from __future__ import annotations

from fastapi import APIRouter

from ..schemas import HealthResponse
from ..state import app_state

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health():
    registry = app_state["registry"]
    return HealthResponse(
        status="ok" if app_state["loaded"] else "standby",
        category=registry.category,
        tool_count=registry.count(),
        loaded=app_state["loaded"],
    )
