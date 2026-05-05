"""
routers/lifecycle.py — /load 和 /unload 端点。

med-calc 无 GPU 权重，/load 只是标记服务就绪，
实现为空操作（no-op），与 Gateway LRU 调度协议保持兼容。
"""
from __future__ import annotations

from fastapi import APIRouter

from ..state import app_state

router = APIRouter()


@router.post("/load", tags=["lifecycle"])
async def load():
    app_state["loaded"] = True
    return {"status": "ok"}


@router.post("/unload", tags=["lifecycle"])
async def unload():
    app_state["loaded"] = False
    return {"status": "unloaded"}
