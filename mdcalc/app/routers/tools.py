"""
routers/tools.py — 工具列表和详情查询。
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..schemas import ParameterInfo, ReturnInfo, ToolDetail, ToolListResponse, ToolSummary
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
                tool_name=t.get("name", fn),
                calc_id=t.get("calc_id"),
                short_description=t.get("short_description"),
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

    parameters = [
        ParameterInfo(
            name=p.get("name", ""),
            type=p.get("type", "Any"),
            description=p.get("description"),
            options=p.get("options") or None,
        )
        for p in tool.get("parameters", [])
    ]

    returns = [
        ReturnInfo(
            key=r.get("key", ""),
            type=r.get("type", "Any"),
            description=r.get("description"),
        )
        for r in tool.get("returns", [])
    ]

    return ToolDetail(
        function_name=function_name,
        tool_name=tool.get("name", function_name),
        calc_id=tool.get("calc_id"),
        slug=tool.get("slug"),
        url=tool.get("url"),
        short_description=tool.get("short_description"),
        full_description=tool.get("full_description"),
        parameters=parameters,
        returns=returns,
        raises=tool.get("raises", []),
        notes=tool.get("notes"),
    )
