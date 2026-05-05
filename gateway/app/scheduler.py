"""
scheduler.py — GPU 显存 LRU 调度器。

职责：
  - 追踪哪些模型当前驻留在 GPU
  - 收到新请求时，若模型未加载则通知对应容器 POST /load
  - 若 GPU 已满，按 LRU 驱逐最久未用的模型（POST /unload）
  - asyncio.Lock 保证并发请求下加载/驱逐操作串行执行
"""
from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, Optional

import httpx


class GPUScheduler:
    def __init__(self, total_gpu_mb: int) -> None:
        self.total_gpu_mb = total_gpu_mb
        # {tool_name: {mb, last_used, endpoint}}
        self._loaded: Dict[str, Dict[str, Any]] = {}
        self._lock: Optional[asyncio.Lock] = None

    def _get_lock(self) -> asyncio.Lock:
        """懒初始化 Lock，确保在事件循环内创建。"""
        if self._lock is None:
            self._lock = asyncio.Lock()
        return self._lock

    def used_mb(self) -> int:
        return sum(v["mb"] for v in self._loaded.values())

    def free_mb(self) -> int:
        return self.total_gpu_mb - self.used_mb()

    def status(self) -> Dict[str, Any]:
        return {
            "total_gpu_mb": self.total_gpu_mb,
            "used_mb": self.used_mb(),
            "free_mb": self.free_mb(),
            "loaded_models": {
                name: {"gpu_mb": v["mb"], "idle_s": round(time.time() - v["last_used"], 1)}
                for name, v in self._loaded.items()
            },
        }

    async def ensure_loaded(self, tool: Dict[str, Any]) -> None:
        """
        确保指定工具的模型已加载进 GPU。
        若 GPU 不足，先按 LRU 驱逐，再加载。
        """
        name = tool["name"]
        async with self._get_lock():
            # 已在 GPU，直接更新使用时间
            if name in self._loaded:
                self._loaded[name]["last_used"] = time.time()
                return

            required_mb = tool.get("gpu_memory_mb", 0)
            endpoint = tool["endpoint"]
            load_timeout = tool.get("load_time_s", 60)

            # LRU 驱逐，直到空间足够
            while self.free_mb() < required_mb and self._loaded:
                victim = min(self._loaded, key=lambda k: self._loaded[k]["last_used"])
                victim_endpoint = self._loaded[victim]["endpoint"]
                print(f"[Scheduler] Evicting '{victim}' to free {self._loaded[victim]['mb']}MB")
                await self._call_unload(victim, victim_endpoint)
                del self._loaded[victim]

            if self.free_mb() < required_mb:
                raise RuntimeError(
                    f"GPU 空间不足：需要 {required_mb}MB，当前剩余 {self.free_mb()}MB"
                )

            # 加载模型
            print(f"[Scheduler] Loading '{name}' ({required_mb}MB) ...")
            await self._call_load(name, endpoint, load_timeout)

            self._loaded[name] = {
                "mb": required_mb,
                "last_used": time.time(),
                "endpoint": endpoint,
            }
            print(f"[Scheduler] '{name}' loaded. GPU used: {self.used_mb()}MB / {self.total_gpu_mb}MB")

    async def _call_load(self, name: str, endpoint: str, timeout: int) -> None:
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(f"{endpoint}/load")
            if resp.status_code not in (200, 201):
                raise RuntimeError(resp.text)
        except Exception as e:
            raise RuntimeError(f"Failed to load '{name}': {e}") from e

    async def _call_unload(self, name: str, endpoint: str) -> None:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                await client.post(f"{endpoint}/unload")
        except Exception as e:
            # 驱逐失败不应阻断流程，记录日志即可
            print(f"[Scheduler] Warning: failed to unload '{name}': {e}")
