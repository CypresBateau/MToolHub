"""
gateway/app/main.py — 统一推理网关入口。

对外只暴露 :9000，通过 tool_name 路由到各 B 类模型容器。
"""
from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncIterator

import httpx
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from .registry import ToolRegistry
from .scheduler import GPUScheduler

# ── 全局单例 ──────────────────────────────────────────────────────────────────
registry = ToolRegistry()
scheduler = GPUScheduler(
    total_gpu_mb=int(os.getenv("TOTAL_GPU_MB", "40000"))
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    registry.scan()
    yield


app = FastAPI(
    title="Medical AI Gateway",
    description="统一推理网关：管理多模型 GPU 调度，对外暴露单一入口。",
    version="1.0.0",
    lifespan=lifespan,
)


# ── 网关健康检查 ───────────────────────────────────────────────────────────────
@app.get("/health", tags=["gateway"])
async def health():
    return {"status": "ok", **scheduler.status()}


# ── 工具列表 ──────────────────────────────────────────────────────────────────
@app.get("/tools", tags=["tools"])
async def list_tools():
    return {
        name: {
            "description": cfg.get("description", ""),
            "type": cfg.get("type"),
            "input": cfg.get("input"),
            "output": cfg.get("output"),
            "gpu_memory_mb": cfg.get("gpu_memory_mb", 0),
            "loaded": name in scheduler._loaded,
        }
        for name, cfg in registry.all().items()
    }


@app.get("/tools/{tool_name}/info", tags=["tools"])
async def tool_info(tool_name: str):
    tool = registry.get(tool_name)
    if not tool:
        raise HTTPException(404, f"Tool '{tool_name}' not found.")
    return tool


# ── 核心推理接口 ───────────────────────────────────────────────────────────────
@app.post("/tools/{tool_name}/predict", tags=["predict"])
async def predict(
    tool_name: str,
    file: UploadFile = File(..., description="输入图像（JPG / PNG / DICOM）"),
    top_k: int = Form(default=5, ge=1, le=75, description="返回概率最高的 K 个结果"),
):
    tool = registry.get(tool_name)
    if not tool:
        available = list(registry.all().keys())
        raise HTTPException(404, f"Tool '{tool_name}' not found. Available: {available}")

    # 确保模型已加载（按需 LRU 调度）
    try:
        await scheduler.ensure_loaded(tool)
    except Exception as e:
        raise HTTPException(503, f"Failed to load model '{tool_name}': {e}")

    # 转发请求到对应容器
    data = await file.read()
    endpoint = tool["endpoint"]
    timeout = tool.get("predict_timeout_s", 60)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(
                f"{endpoint}/api/v1/predict",
                files={"file": (file.filename or "upload", data)},
                data={"top_k": str(top_k)},
            )
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except httpx.TimeoutException:
        raise HTTPException(504, f"Inference timeout for '{tool_name}' (>{timeout}s)")
    except Exception as e:
        raise HTTPException(502, f"Error calling '{tool_name}': {e}")


# ── JSON 工具调用接口（计算器 / 单位换算）─────────────────────────────────────
@app.post("/tools/{tool_name}/call", tags=["call"])
async def call_tool(tool_name: str, request: Request):
    tool = registry.get(tool_name)
    if not tool:
        available = list(registry.all().keys())
        raise HTTPException(404, f"Tool '{tool_name}' not found. Available: {available}")

    try:
        await scheduler.ensure_loaded(tool)
    except Exception as e:
        raise HTTPException(503, f"Failed to load tool '{tool_name}': {e}")

    body = await request.json()
    endpoint = tool["endpoint"]
    timeout = tool.get("call_timeout_s", 30)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(f"{endpoint}/api/v1/call", json=body)
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except httpx.TimeoutException:
        raise HTTPException(504, f"Call timeout for '{tool_name}' (>{timeout}s)")
    except Exception as e:
        raise HTTPException(502, f"Error calling '{tool_name}': {e}")
