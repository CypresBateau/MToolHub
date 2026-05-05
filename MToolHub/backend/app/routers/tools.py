"""
工具管理路由
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from app.core.registry import registry_manager

router = APIRouter()


@router.get("/api/tools")
async def list_tools(
    category: Optional[str] = Query(None, description="类别过滤：tool/model/skill"),
    tag: Optional[str] = Query(None, description="标签过滤"),
    limit: int = Query(20, ge=1, le=100, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
):
    """
    获取工具列表

    支持分页和过滤
    """
    resources = registry_manager.get_all_resources()

    # 类别过滤
    if category:
        resources = [r for r in resources if r["category"] == category]

    # 标签过滤
    if tag:
        resources = [
            r for r in resources if tag in r["item"].get("tags", [])
        ]

    total = len(resources)
    resources = resources[offset : offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": resources,
    }


@router.get("/api/tools/{resource_id}")
async def get_tool_detail(resource_id: str):
    """
    获取工具详情
    """
    resource = registry_manager.get_resource_by_id(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail=f"资源不存在：{resource_id}")

    return resource
