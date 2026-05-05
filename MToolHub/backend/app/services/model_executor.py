"""
模型执行器

负责调用 Gateway 的 /predict 接口执行 AI 模型推理
"""

import httpx
from typing import Dict, Any, Optional
from app.services.executor import Executor
from app.core.claude_client import claude_client
from app.config import settings


class ModelExecutor(Executor):
    """模型执行器"""

    def __init__(self):
        self.gateway_base_url = settings.gateway_base_url
        self.timeout = settings.gateway_timeout

    async def execute(
        self,
        resource: Dict[str, Any],
        user_message: str,
        arguments: Optional[Dict[str, Any]] = None,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None,
        conversation_history: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        执行模型推理

        流程：
        1. 检查是否有文件上传
        2. 调用 Gateway /predict 接口
        3. 使用 Claude 解读结果
        """
        trace = []

        # 步骤 1：检查文件
        if not file_bytes:
            return {
                "success": False,
                "response": f"该功能需要上传{resource.get('input_type', '文件')}，请上传后重试。",
                "result": None,
                "trace": "缺少文件输入",
            }

        # 步骤 2：调用 Gateway
        trace.append(f"正在调用 {resource['gateway_tool_name']} 模型...")
        try:
            # 获取参数
            params = arguments or {}
            top_k = params.get("top_k", resource.get("parameters", {}).get("top_k", {}).get("default", 5))

            result = await self._call_gateway(
                gateway_tool_name=resource["gateway_tool_name"],
                file_bytes=file_bytes,
                filename=filename,
                top_k=top_k,
            )
            trace.append(f"模型推理成功")
        except Exception as e:
            trace.append(f"模型推理失败：{e}")
            return {
                "success": False,
                "response": f"模型推理失败：{e}",
                "result": None,
                "trace": "\n".join(trace),
            }

        # 步骤 3：解读结果
        trace.append("正在解读结果...")
        interpretation = await claude_client.interpret_result(
            user_message=user_message,
            tool_result=result,
            tool_name=resource["name"],
            conversation_history=conversation_history,
        )
        trace.append("解读完成")

        return {
            "success": True,
            "response": interpretation,
            "result": result,
            "trace": "\n".join(trace),
        }

    async def _call_gateway(
        self,
        gateway_tool_name: str,
        file_bytes: bytes,
        filename: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        调用 Gateway /predict 接口

        Args:
            gateway_tool_name: Gateway 中的工具名（如 mavl）
            file_bytes: 文件字节
            filename: 文件名
            top_k: 返回 top-k 预测结果

        Returns:
            Gateway 返回的结果
        """
        url = f"{self.gateway_base_url}/tools/{gateway_tool_name}/predict"

        files = {"file": (filename, file_bytes)}
        data = {"top_k": str(top_k)}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, files=files, data=data)
            response.raise_for_status()
            return response.json()


# 全局模型执行器实例
model_executor = ModelExecutor()
