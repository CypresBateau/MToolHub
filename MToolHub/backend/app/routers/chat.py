"""
对话接口路由
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.models.api import ChatResponse
from app.services.router import route_decision_maker
from app.services.orchestrator import orchestrator
from app.utils.disclaimer import get_disclaimer

router = APIRouter()


@router.post("/api/chat", response_model=ChatResponse)
async def chat(
    message: str = Form(..., description="用户消息"),
    file: Optional[UploadFile] = File(None, description="上传的文件（可选）"),
    conversation_id: Optional[str] = Form(None, description="会话 ID（可选）"),
):
    """
    对话接口

    支持：
    - 纯文本对话
    - 文本 + 文件（如胸片图像）

    流程：
    1. 路由决策：根据用户消息和文件类型决定调用策略
    2. 执行：调用相应的工具/模型/技能
    3. 返回：包含回复、使用的资源、路由信息
    """
    # 读取文件（如有）
    file_bytes = None
    filename = None
    file_type = None

    if file:
        file_bytes = await file.read()
        filename = file.filename
        file_type = file.content_type

    # 路由决策
    routing_plan = route_decision_maker.decide(
        user_message=message,
        has_file=file is not None,
        file_type=file_type,
    )

    # 执行
    try:
        result = await orchestrator.run(
            user_message=message,
            routing_plan=routing_plan,
            file_bytes=file_bytes,
            filename=filename,
            conversation_history=None,  # TODO: 从 conversation_id 恢复历史
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行失败：{str(e)}")

    # 构建响应
    return ChatResponse(
        response=result["response"],
        tools_used=result.get("tools_used", []),
        routing_info={
            "mode": routing_plan.mode,
            "confidence": routing_plan.confidence,
            "candidates": [r["item"]["name"] for r in routing_plan.selected_resources],
            "trace": result.get("trace", ""),
        },
        disclaimer=get_disclaimer(),
    )
