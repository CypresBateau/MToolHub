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
    result: Dict[str, Any]          # mdcalc 工具统一返回 dict


# ── 参数 / 返回值子结构 ───────────────────────────────────────────────────────

class ParameterInfo(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    options: Optional[str] = None   # 枚举选项或取值范围说明


class ReturnInfo(BaseModel):
    key: str
    type: str
    description: Optional[str] = None


# ── 工具信息 ──────────────────────────────────────────────────────────────────

class ToolSummary(BaseModel):
    function_name: str
    tool_name: str
    calc_id: Optional[str] = None
    short_description: Optional[str] = None


class ToolDetail(BaseModel):
    function_name: str
    tool_name: str
    calc_id: Optional[str] = None
    slug: Optional[str] = None
    url: Optional[str] = None
    short_description: Optional[str] = None
    full_description: Optional[str] = None
    parameters: List[ParameterInfo] = []
    returns: List[ReturnInfo] = []
    raises: List[str] = []
    notes: Optional[str] = None


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
