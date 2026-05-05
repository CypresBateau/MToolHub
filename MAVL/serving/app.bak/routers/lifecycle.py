"""lifecycle.py — /load 和 /unload 接口，由 Gateway 调度器调用。"""
from __future__ import annotations

import torch
from fastapi import APIRouter

from ..model_singleton import ModelSingleton

router = APIRouter(tags=["lifecycle"])


@router.post("/load")
async def load():
    """将模型权重加载进 GPU。已加载时直接返回。"""
    sg = ModelSingleton.get()
    if sg.loaded:
        return {"status": "already_loaded"}
    sg.load()
    return {"status": "loaded"}


@router.post("/unload")
async def unload():
    """释放 GPU 显存。由 Gateway LRU 调度器在驱逐时调用。"""
    sg = ModelSingleton.get()
    sg.unload()
    return {"status": "unloaded"}
