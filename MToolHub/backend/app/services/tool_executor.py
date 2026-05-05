"""
工具执行器

负责调用 Gateway 的 /call 接口执行医疗计算工具
"""

import httpx
from typing import Dict, Any, Optional
from app.services.executor import Executor
from app.core.claude_client import claude_client
from app.config import settings


class ToolExecutor(Executor):
    """工具执行器"""

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
        执行工具调用

        流程：
        1. 如果没有提供 arguments，使用 Claude 从 user_message 中提取参数
        2. 调用 Gateway /call 接口
        3. 使用 Claude 解读结果
        """
        trace = []

        # 步骤 1：提取参数
        if arguments is None:
            trace.append("正在从用户消息中提取参数...")
            arguments = await claude_client.extract_parameters(
                user_message=user_message,
                tool_schema=resource["input_schema"],
                conversation_history=conversation_history,
            )

            if arguments is None:
                # Claude 没有调用工具，可能在追问参数
                return {
                    "success": False,
                    "response": "请提供更多信息以便我帮您计算。",
                    "result": None,
                    "trace": "\n".join(trace),
                }

            trace.append(f"提取的参数：{arguments}")

        # 步骤 2：调用 Gateway
        trace.append(f"正在调用 {resource['gateway_tool_name']}...")
        try:
            result = await self._call_gateway(
                gateway_tool_name=resource["gateway_tool_name"],
                function_name=resource["function_name"],
                arguments=arguments,
            )
            trace.append(f"调用成功")
        except Exception as e:
            trace.append(f"调用失败：{e}")
            return {
                "success": False,
                "response": f"工具调用失败：{e}",
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
        function_name: str,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        调用 Gateway /call 接口

        Args:
            gateway_tool_name: Gateway 中的工具名（如 tool-mdcalc）
            function_name: 函数名
            arguments: 参数字典

        Returns:
            Gateway 返回的结果
        """
        url = f"{self.gateway_base_url}/tools/{gateway_tool_name}/call"
        payload = {
            "function_name": function_name,
            "arguments": arguments,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()


# 全局工具执行器实例
tool_executor = ToolExecutor()
