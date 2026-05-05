"""
路由决策模块

根据向量检索结果决定调用策略
"""

from typing import Dict, Any, Optional
from app.models.api import RoutingPlan
from app.core.faiss_index import vector_search_engine
from app.config import settings


class RouteDecisionMaker:
    """
    路由决策器

    根据向量检索的置信度分数，决定三种调用模式：
    1. direct_call (score ≥ 0.85): 高置信度，直接执行匹配的资源
    2. claude_select (0.60 ≤ score < 0.85): 中置信度，将 top-3 候选传给 Claude 选择
    3. chat_only (score < 0.60): 低置信度，纯对话模式
    """

    def __init__(self):
        self.threshold_high = settings.direct_call_threshold
        self.threshold_low = settings.claude_select_threshold

    def decide(
        self,
        user_message: str,
        has_file: bool = False,
        file_type: Optional[str] = None,
        top_k: int = 5,
    ) -> RoutingPlan:
        """
        路由决策

        Args:
            user_message: 用户消息
            has_file: 是否有附件
            file_type: 文件类型（如 image/jpeg）
            top_k: 检索结果数量

        Returns:
            RoutingPlan 对象
        """
        # 向量检索
        results = vector_search_engine.search(user_message, top_k=top_k)

        # 如果有图像文件，强制将图像模型加入候选
        if has_file and file_type and file_type.startswith("image"):
            image_results = vector_search_engine.search(
                user_message, top_k=2, categories=["model"]
            )
            # 合并结果，去重
            seen_ids = set()
            merged_results = []
            for r in image_results + results:
                item_id = r["item"].get("id")
                if item_id not in seen_ids:
                    seen_ids.add(item_id)
                    merged_results.append(r)
            results = merged_results[:top_k]

        # 如果没有结果或分数太低，走纯对话模式
        if not results or results[0]["score"] < self.threshold_low:
            return RoutingPlan(
                mode="chat_only",
                confidence="low",
                selected_resources=[],
            )

        # 高置信度：直接调用
        if results[0]["score"] >= self.threshold_high:
            return RoutingPlan(
                mode="direct_call",
                confidence="high",
                selected_resources=[results[0]],
            )

        # 中置信度：让 Claude 从 top-3 中选择
        return RoutingPlan(
            mode="claude_select",
            confidence="medium",
            selected_resources=results[:3],
        )


# 全局路由决策器实例
route_decision_maker = RouteDecisionMaker()
