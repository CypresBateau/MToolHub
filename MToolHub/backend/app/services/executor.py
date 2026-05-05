"""
执行器基类

定义所有执行器的通用接口
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class Executor(ABC):
    """执行器基类"""

    @abstractmethod
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
        执行资源调用

        Args:
            resource: 资源元数据
            user_message: 用户消息
            arguments: 执行参数（可选，如果提供则直接使用）
            file_bytes: 文件字节（用于模型）
            filename: 文件名（用于模型）
            conversation_history: 对话历史

        Returns:
            执行结果字典：
            {
                "success": bool,
                "response": str,  # 给用户的回复
                "result": Any,    # 原始结果
                "trace": str,     # 执行追踪
            }
        """
        pass
