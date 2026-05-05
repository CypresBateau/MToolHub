"""POST /api/v1/predict — 上传图片，返回 75 种疾病概率。"""
from __future__ import annotations

import os
import time
import uuid

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..inference import run_inference
from ..model_singleton import ORIGINAL_CLASS, ModelSingleton
from ..schemas import DiseasePrediction, PredictResponse

router = APIRouter()

_MAX_BYTES_DEFAULT = 20 * 1024 * 1024  # 20 MB


@router.post("/api/v1/predict", response_model=PredictResponse, tags=["predict"])
async def predict(
    file: UploadFile = File(..., description="胸片文件（JPG / PNG / DICOM）"),
    top_k: int = Form(default=5, ge=1, le=75, description="返回概率最高的 K 个疾病"),
) -> PredictResponse:
    sg = ModelSingleton.get()
    if not sg.loaded:
        raise HTTPException(status_code=503, detail="Model is still loading, please retry.")

    max_bytes = int(os.environ.get("MAX_FILE_SIZE_MB", 20)) * 1024 * 1024
    data = await file.read()
    if len(data) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(data) // 1024} KB). Max allowed: {max_bytes // 1024 // 1024} MB.",
        )

    filename = file.filename or "upload"
    lower = filename.lower()
    if not any(lower.endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".dcm")):
        raise HTTPException(
            status_code=415,
            detail="Unsupported file type. Accepted: jpg, jpeg, png, dcm.",
        )

    t0 = time.perf_counter()
    probs: list[float] = run_inference(data, filename, sg)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    all_preds = [
        DiseasePrediction(disease=name, probability=round(p, 6))
        for name, p in zip(ORIGINAL_CLASS, probs)
    ]

    sorted_preds = sorted(all_preds, key=lambda x: x.probability, reverse=True)

    return PredictResponse(
        request_id=str(uuid.uuid4()),
        filename=filename,
        inference_time_ms=round(elapsed_ms, 2),
        predictions=all_preds,
        top_k=sorted_preds[:top_k],
        model_info={
            "checkpoint": sg.checkpoint_name,
            "mode": sg.mode,
            "device": str(sg.device),
        },
    )
