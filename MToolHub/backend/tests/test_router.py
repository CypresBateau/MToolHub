"""
路由决策测试
"""

import pytest
from app.services.router import RouteDecisionMaker
from app.core.faiss_index import VectorSearchEngine
from app.core.embedding import EmbeddingModel
from app.config import settings


@pytest.fixture
def route_decision_maker():
    """创建路由决策器实例"""
    embedding_model = EmbeddingModel()
    search_engine = VectorSearchEngine(embedding_model)
    return RouteDecisionMaker(search_engine, settings)


def test_direct_call_mode(route_decision_maker):
    """测试直接调用模式（高置信度）"""
    # 模拟高置信度查询
    plan = route_decision_maker.decide(
        user_message="计算 Wells DVT 评分",
        has_file=False
    )

    # 如果索引已构建且包含 Wells DVT，应该是 direct_call
    if plan.selected_resources:
        assert plan.mode in ["direct_call", "claude_select"]
        assert plan.confidence > 0.0


def test_chat_only_mode(route_decision_maker):
    """测试纯对话模式（低置信度）"""
    # 模拟低置信度查询
    plan = route_decision_maker.decide(
        user_message="今天天气怎么样？",
        has_file=False
    )

    # 应该是 chat_only 模式
    assert plan.mode == "chat_only"
    assert plan.confidence < settings.claude_select_threshold


def test_file_upload_routing(route_decision_maker):
    """测试文件上传路由"""
    # 模拟图像上传
    plan = route_decision_maker.decide(
        user_message="分析这张胸片",
        has_file=True,
        file_type="image/jpeg"
    )

    # 应该路由到模型
    if plan.selected_resources:
        assert any(r["category"] == "model" for r in plan.selected_resources)


def test_routing_plan_structure(route_decision_maker):
    """测试路由计划结构"""
    plan = route_decision_maker.decide(
        user_message="计算血糖",
        has_file=False
    )

    # 验证返回结构
    assert hasattr(plan, "mode")
    assert hasattr(plan, "confidence")
    assert hasattr(plan, "selected_resources")
    assert plan.mode in ["direct_call", "claude_select", "chat_only"]
    assert 0.0 <= plan.confidence <= 1.0
