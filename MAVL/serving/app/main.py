"""
serving/app/main.py — FastAPI 应用入口。

启动时只启动 HTTP server，不加载模型（等待 Gateway 调用 /load）。
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from .routers import health, predict
from .routers import lifecycle


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # 不在启动时加载模型，由 Gateway 按需调用 /load
    print("[MAVL] Server ready. Waiting for /load call from Gateway.")
    yield


app = FastAPI(
    title="MAVL Inference Service",
    description="零样本胸片分类推理服务（B类容器，由 Gateway 统一调度）",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(lifecycle.router)
app.include_router(predict.router)
