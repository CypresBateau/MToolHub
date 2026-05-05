"""
编排器（Orchestrator）

根据路由计划编排执行流程
"""

from typing import Dict, Any, Optional
from app.models.api import RoutingPlan
from app.services.tool_executor import tool_executor
from app.services.model_executor import model_executor
from app.services.skill_executor import skill_executor
from app.core.claude_client import claude_client
from app.config import settings


class Orchestrator:
    """
    编排器

    根据 RoutingPlan 决定执行策略：
    1. chat_only: 纯对话，不调用任何资源
    2. direct_call: 直接执行选定的资源
    3. claude_select: 将候选资源作为 tools 传给 Claude，让 Claude 选择
    """

    def __init__(self):
        self.tool_executor = tool_executor
        self.model_executor = model_executor
        self.skill_executor = skill_executor
        self.claude_client = claude_client

    async def run(
        self,
        user_message: str,
        routing_plan: RoutingPlan,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None,
        conversation_history: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        执行编排

        Args:
            user_message: 用户消息
            routing_plan: 路由计划
            file_bytes: 文件字节（可选）
            filename: 文件名（可选）
            conversation_history: 对话历史（可选）

        Returns:
            执行结果字典：
            {
                "response": str,           # 给用户的回复
                "tools_used": List[str],   # 使用的资源 ID 列表
                "mode": str,               # 执行模式
                "trace": str,              # 执行追踪
            }
        """
        if routing_plan.mode == "chat_only":
            return await self._chat_only(user_message, conversation_history)

        elif routing_plan.mode == "direct_call":
            resource = routing_plan.selected_resources[0]
            return await self._direct_execute(
                resource, user_message, file_bytes, filename, conversation_history
            )

        elif routing_plan.mode == "claude_select":
            return await self._claude_select(
                routing_plan.selected_resources,
                user_message,
                file_bytes,
                filename,
                conversation_history,
            )

        else:
            return {
                "response": f"未知的路由模式：{routing_plan.mode}",
                "tools_used": [],
                "mode": "error",
                "trace": "",
            }

    async def _chat_only(
        self, user_message: str, conversation_history: Optional[list]
    ) -> Dict[str, Any]:
        """纯对话模式"""
        messages = conversation_history or []
        messages.append({"role": "user", "content": user_message})

        system = (
            "你是一个专业的医疗助手。如果用户的问题涉及具体的计算或诊断，"
            "建议他们提供更多信息以便调用专业工具。"
            f"\n\n{settings.medical_disclaimer}"
        )

        response = await self.claude_client.chat(messages=messages, system=system)

        response_text = ""
        for block in response.content:
            if block.type == "text":
                response_text += block.text

        return {
            "response": response_text,
            "tools_used": [],
            "mode": "chat_only",
            "trace": "纯对话模式，未调用任何工具",
        }

    async def _direct_execute(
        self,
        resource: Dict[str, Any],
        user_message: str,
        file_bytes: Optional[bytes],
        filename: Optional[str],
        conversation_history: Optional[list],
    ) -> Dict[str, Any]:
        """直接执行模式"""
        item = resource["item"]
        category = resource["category"]

        # 根据类别选择执行器
        if category == "tool":
            executor = self.tool_executor
        elif category == "model":
            executor = self.model_executor
        elif category == "skill":
            executor = self.skill_executor
        else:
            return {
                "response": f"未知的资源类别：{category}",
                "tools_used": [],
                "mode": "error",
                "trace": "",
            }

        # 执行
        result = await executor.execute(
            resource=item,
            user_message=user_message,
            file_bytes=file_bytes,
            filename=filename,
            conversation_history=conversation_history,
        )

        return {
            "response": result["response"],
            "tools_used": [item["id"]] if result["success"] else [],
            "mode": "direct_call",
            "trace": result["trace"],
        }

    async def _claude_select(
        self,
        candidates: list,
        user_message: str,
        file_bytes: Optional[bytes],
        filename: Optional[str],
        conversation_history: Optional[list],
    ) -> Dict[str, Any]:
        """Claude 选择模式"""
        # 构建工具列表
        tools = []
        for candidate in candidates:
            item = candidate["item"]
            category = candidate["category"]

            if category == "tool":
                # 工具类型：使用 input_schema
                tools.append({
                    "name": item["id"],
                    "description": f"{item['name']}: {item['description']}",
                    "input_schema": item["input_schema"],
                })
            elif category == "model":
                # 模型类型：简化的 schema
                tools.append({
                    "name": item["id"],
                    "description": f"{item['name']}: {item['description']}. 需要上传{item['input_type']}文件。",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "confirm": {
                                "type": "boolean",
                                "description": "确认使用此模型",
                            }
                        },
                        "required": ["confirm"],
                    },
                })
            elif category == "skill":
                # 技能类型：简化的 schema
                tools.append({
                    "name": item["id"],
                    "description": f"{item['name']}: {item['description']}",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "confirm": {
                                "type": "boolean",
                                "description": "确认使用此技能",
                            }
                        },
                        "required": ["confirm"],
                    },
                })

        # 调用 Claude 让它选择
        messages = conversation_history or []
        messages.append({"role": "user", "content": user_message})

        system = (
            "你是医疗助手。请根据用户的需求，从提供的工具中选择最合适的一个。"
            f"\n\n{settings.medical_disclaimer}"
        )

        response = await self.claude_client.chat(
            messages=messages, system=system, tools=tools
        )

        # 检查 Claude 是否选择了工具
        if response.stop_reason == "tool_use":
            for block in response.content:
                if block.type == "tool_use":
                    # 找到对应的资源
                    selected_id = block.name
                    selected_resource = None
                    for candidate in candidates:
                        if candidate["item"]["id"] == selected_id:
                            selected_resource = candidate
                            break

                    if selected_resource:
                        # 执行选中的资源
                        return await self._direct_execute(
                            selected_resource,
                            user_message,
                            file_bytes,
                            filename,
                            conversation_history,
                        )

        # Claude 没有选择工具，返回对话
        response_text = ""
        for block in response.content:
            if block.type == "text":
                response_text += block.text

        return {
            "response": response_text,
            "tools_used": [],
            "mode": "claude_select",
            "trace": "Claude 未选择任何工具",
        }


# 全局编排器实例
orchestrator = Orchestrator()
