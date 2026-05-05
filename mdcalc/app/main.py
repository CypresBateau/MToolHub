"""
main.py — mdcalc FastAPI 应用入口。

启动时从 TOOL_JSON_PATH 加载 tools_metadata.json（纯 CPU，无 GPU 依赖）。
/load 和 /unload 端点仅做状态标记，与 Gateway LRU 调度协议保持兼容。
"""
from __future__ import annotations

import os
import sys
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from .routers import call, health, lifecycle, tools
from .state import app_state
from .tool_registry import ToolRegistry


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    json_path = os.getenv("TOOL_JSON_PATH", "")
    if not json_path:
        print("[mdcalc] ERROR: TOOL_JSON_PATH is not set.", file=sys.stderr)
        sys.exit(1)

    registry = ToolRegistry()
    try:
        registry.load(json_path)
    except Exception as e:
        print(f"[mdcalc] ERROR: Failed to load tools: {e}", file=sys.stderr)
        sys.exit(1)

    app_state["registry"] = registry
    app_state["loaded"] = True
    print(f"[mdcalc] Ready. category={registry.category}, tools={registry.count()}")
    yield


app = FastAPI(
    title="MDCalc Tool Service",
    description="871 个 MDCalc 医疗计算器工具执行服务（CPU，由 Gateway 统一调度）",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(lifecycle.router)
app.include_router(tools.router)
app.include_router(call.router)
