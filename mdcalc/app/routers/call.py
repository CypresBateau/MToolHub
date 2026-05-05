"""
routers/call.py — 工具执行端点。
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..executor import run_tool
from ..schemas import CallRequest, CallResponse
from ..state import app_state

router = APIRouter(prefix="/api/v1", tags=["call"])


@router.post("/call", response_model=CallResponse)
async def call_tool(req: CallRequest):
    registry = app_state["registry"]
    tool = registry.get(req.function_name)
    if not tool:
        raise HTTPException(404, f"Tool '{req.function_name}' not found.")

    try:
        result = run_tool(tool, req.arguments)
    except ValueError as e:
        raise HTTPException(422, f"Validation error: {e}")
    except TypeError as e:
        raise HTTPException(422, f"Argument error: {e}")
    except Exception as e:
        raise HTTPException(500, f"Execution error: {e}")

    return CallResponse(
        function_name=req.function_name,
        tool_name=tool.get("name", req.function_name),
        category=registry.category,
        result=result,
    )
