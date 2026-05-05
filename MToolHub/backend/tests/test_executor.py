"""
执行器测试
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.tool_executor import ToolExecutor
from app.services.model_executor import ModelExecutor
from app.services.skill_executor import SkillExecutor


@pytest.fixture
def tool_executor():
    """创建工具执行器实例"""
    return ToolExecutor()


@pytest.fixture
def model_executor():
    """创建模型执行器实例"""
    return ModelExecutor()


@pytest.fixture
def skill_executor():
    """创建技能执行器实例"""
    return SkillExecutor()


@pytest.mark.asyncio
async def test_tool_executor_with_arguments(tool_executor):
    """测试工具执行器（提供参数）"""
    resource = {
        "resource_id": "tool-mdcalc:test_tool",
        "gateway_tool_name": "tool-mdcalc",
        "function_name": "test_function",
        "parameters": []
    }

    arguments = {"param1": 1, "param2": 2}

    # Mock Gateway 调用
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "success"}
        mock_response.raise_for_status = MagicMock()

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        # Mock Claude 调用
        with patch("app.services.tool_executor.claude_client") as mock_claude:
            mock_claude.interpret_result = AsyncMock(
                return_value="测试结果解释"
            )

            result = await tool_executor.execute(
                resource=resource,
                user_message="测试消息",
                arguments=arguments
            )

            assert result["success"] == True
            assert "result" in result


@pytest.mark.asyncio
async def test_model_executor_without_file(model_executor):
    """测试模型执行器（无文件）"""
    resource = {
        "resource_id": "model:test_model",
        "gateway_tool_name": "test_model",
        "input_type": "image"
    }

    result = await model_executor.execute(
        resource=resource,
        user_message="测试消息",
        file_bytes=None
    )

    # 应该返回错误
    assert result["success"] == False
    assert "error" in result


@pytest.mark.asyncio
async def test_skill_executor_document_only(skill_executor):
    """测试技能执行器（document_only 类型）"""
    resource = {
        "resource_id": "skill:test_skill",
        "skill_type": "document_only",
        "skill_md_path": "tests/fixtures/test_skill.md"
    }

    # 创建测试文件
    import os
    os.makedirs("tests/fixtures", exist_ok=True)
    with open("tests/fixtures/test_skill.md", "w", encoding="utf-8") as f:
        f.write("# 测试技能\n\n这是一个测试技能。")

    # Mock Claude 调用
    with patch("app.services.skill_executor.claude_client") as mock_claude:
        mock_claude.chat = AsyncMock(
            return_value="技能执行结果"
        )

        result = await skill_executor.execute(
            resource=resource,
            user_message="测试消息"
        )

        assert result["success"] == True
        assert "result" in result

    # 清理测试文件
    os.remove("tests/fixtures/test_skill.md")


def test_executor_interface():
    """测试执行器接口"""
    from app.services.executor import Executor
    import inspect

    # 验证抽象方法
    assert inspect.isabstract(Executor)
    assert hasattr(Executor, "execute")
