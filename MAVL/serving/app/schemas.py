"""Pydantic schemas for request / response."""
from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field


class DiseasePrediction(BaseModel):
    disease: str
    probability: float = Field(..., ge=0.0, le=1.0)


class PredictResponse(BaseModel):
    request_id: str
    filename: str
    inference_time_ms: float
    predictions: List[DiseasePrediction]
    top_k: List[DiseasePrediction]
    model_info: Dict[str, str]


class HealthResponse(BaseModel):
    status: str               # "ok" | "standby" | "error"
    model_loaded: bool
    checkpoint: str
    device: str
    mode: str
    gpu_memory_mb: int = 0    # 当前占用显存（MB），未加载时为 0
