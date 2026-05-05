"""
直接执行接口路由
"""

from fastapi import APIRouter, HTTPException
from app.models.api import ExecuteRequest, ExecuteResponse
from app.core.registry import registry_manager
from app.services.tool_executor import tool_executor
from app.services.model_executor import model_executor
from app.services.skill_executor import skill_executor
from app.utils.disclaimer import get_disclaimer

router = APIRouter()


@router.post("/api/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest):
    """
    直接执行接口

    用于已知资源 ID 和参数的情况，直接调用资源

    示例：
    ```json
    {
        "resource_id": "tool_mdcalc_wells_dvt",
        "arguments": {
            "active_cancer": 0,
            "paralysis": 0,
            "recent_immobilization": 1,
            "localized_tenderness": 1,
            "entire_leg_swelling": 0,
            "calf_swelling": 0,
            "pitting_edema": 0,
            "collateral_veins": 0,
            "alternative_diagnosis": 0
        },
        "context": "患者最近卧床3天"
    }
    ```
    """
    # 查找资源
    resource_info = registry_manager.get_resource_by_id(request.resource_id)
    if not resource_info:
        raise HTTPException(status_code=404, detail=f"资源不存在：{request.resource_id}")

    category = resource_info["category"]
    item = resource_info["item"]

    # 选择执行器
    if category == "tool":
        executor = tool_executor
    elif category == "model":
        executor = model_executor
    elif category == "skill":
        executor = skill_executor
    else:
        raise HTTPException(status_code=400, detail=f"未知的资源类别：{category}")

    # 执行
    try:
        # 将 item 转换为字典
        if hasattr(item, "model_dump"):
            item_dict = item.model_dump()
        else:
            item_dict = item

        result = await executor.execute(
            resource=item_dict,
            user_message=request.context or "",
            arguments=request.arguments,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行失败：{str(e)}")

    return ExecuteResponse(
        success=result["success"],
        result=result["result"],
        trace=result.get("trace"),
        disclaimer=get_disclaimer(),
    )
