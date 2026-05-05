"""
routers/tools.py — 工具列表和详情查询。
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..schemas import ToolDetail, ToolListResponse, ToolSummary
from ..state import app_state

router = APIRouter(prefix="/api/v1", tags=["tools"])


@router.get("/tools", response_model=ToolListResponse)
async def list_tools():
    registry = app_state["registry"]
    return ToolListResponse(
        category=registry.category,
        count=registry.count(),
        tools=[
            ToolSummary(
                function_name=fn,
                tool_name=t.get("tool_name", fn),
                description=t.get("description"),
            )
            for fn, t in registry.all().items()
        ],
    )


@router.get("/tools/{function_name}", response_model=ToolDetail)
async def get_tool(function_name: str):
    registry = app_state["registry"]
    tool = registry.get(function_name)
    if not tool:
        raise HTTPException(404, f"Tool '{function_name}' not found.")
    return ToolDetail(
        function_name=function_name,
        tool_name=tool.get("tool_name", function_name),
        description=tool.get("description"),
        formula=tool.get("formula"),
        docstring=tool.get("docstring"),
        next_steps=tool.get("next_steps"),
    )
