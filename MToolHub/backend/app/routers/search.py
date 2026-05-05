"""
工具搜索路由
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from app.models.api import ToolSearchRequest, ToolSearchResponse
from app.core.faiss_index import vector_search_engine

router = APIRouter()


@router.get("/api/tools/search", response_model=ToolSearchResponse)
async def search_tools(
    q: str = Query(..., description="搜索查询"),
    top_k: int = Query(5, ge=1, le=20, description="返回结果数量"),
    categories: Optional[str] = Query(None, description="限定类别，逗号分隔，如 tool,model"),
):
    """
    语义搜索工具/模型/技能

    使用向量检索进行语义匹配
    """
    # 解析类别
    category_list = None
    if categories:
        category_list = [c.strip() for c in categories.split(",")]
        # 验证类别
        valid_categories = {"tool", "model", "skill"}
        for cat in category_list:
            if cat not in valid_categories:
                raise HTTPException(
                    status_code=400,
                    detail=f"无效的类别：{cat}，有效值为 tool, model, skill",
                )

    # 向量搜索
    results = vector_search_engine.search(
        query=q,
        top_k=top_k,
        categories=category_list,
    )

    return ToolSearchResponse(
        results=results,
        total=len(results),
    )
