"""
serving/app/main.py — FastAPI 应用入口。

lifespan 启动钩子在进程启动时加载模型（一次），失败则 sys.exit(1)
触发 Docker restart policy，避免留下无效进程。
"""
from __future__ import annotations

import sys
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from .model_singleton import ModelSingleton
from .routers import health, predict


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """启动时加载模型；关闭时清理（GPU 显存由 PyTorch 自动释放）。"""
    try:
        ModelSingleton.get().load()
    except Exception as exc:
        print(f"[FATAL] Failed to load MAVL model: {exc}", file=sys.stderr)
        sys.exit(1)
    yield
    # shutdown：暂无需显式清理


app = FastAPI(
    title="MAVL Inference Service",
    description="零样本胸片分类推理服务，支持 JPG / PNG / DICOM 上传，返回 75 种疾病概率。",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(predict.router)
