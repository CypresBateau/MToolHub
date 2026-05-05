"""GET /health — 服务健康检查，返回模型加载状态和当前 GPU 占用。"""
from __future__ import annotations

import torch
from fastapi import APIRouter

from ..model_singleton import ModelSingleton
from ..schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health() -> HealthResponse:
    sg = ModelSingleton.get()
    gpu_mb = 0
    if sg.loaded and sg.device and sg.device.type == "cuda":
        gpu_mb = torch.cuda.memory_allocated(sg.device) // (1024 * 1024)
    return HealthResponse(
        status="ok" if sg.loaded else "standby",
        model_loaded=sg.loaded,
        checkpoint=sg.checkpoint_name,
        device=str(sg.device) if sg.device else "unknown",
        mode=sg.mode,
        gpu_memory_mb=gpu_mb,
    )
