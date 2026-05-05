"""
routers/lifecycle.py — Gateway LRU 协议兼容的 load / unload 端点。

mdcalc 是纯 CPU 服务，无需真正加载 / 卸载模型，
端点仅翻转 loaded 标志以满足 Gateway 调度协议。
"""
from __future__ import annotations

from fastapi import APIRouter

from ..state import app_state

router = APIRouter(tags=["lifecycle"])


@router.post("/load")
async def load():
    app_state["loaded"] = True
    return {"status": "ok"}


@router.post("/unload")
async def unload():
    app_state["loaded"] = False
    return {"status": "unloaded"}
