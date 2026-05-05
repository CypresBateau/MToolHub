"""
schemas.py — 请求 / 响应数据模型。
使用 pydantic v1（<2.0）兼容写法。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


# ── 调用工具 ──────────────────────────────────────────────────────────────────

class CallRequest(BaseModel):
    function_name: str
    arguments: Dict[str, Any]


class CallResponse(BaseModel):
    function_name: str
    tool_name: str
    category: str
    result: Any


# ── 工具信息 ──────────────────────────────────────────────────────────────────

class ToolSummary(BaseModel):
    function_name: str
    tool_name: str
    description: Optional[str] = None


class ToolDetail(BaseModel):
    function_name: str
    tool_name: str
    description: Optional[str] = None
    formula: Optional[str] = None
    docstring: Optional[str] = None
    next_steps: Optional[str] = None


class ToolListResponse(BaseModel):
    category: str
    count: int
    tools: List[ToolSummary]


# ── 健康检查 ──────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str          # "ok" | "standby"
    category: str
    tool_count: int
    loaded: bool
