"""
测试配置
"""

import pytest
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def test_data_dir():
    """测试数据目录"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def sample_tool():
    """示例工具元数据"""
    return {
        "resource_id": "tool-test:sample_tool",
        "resource_type": "tool",
        "name": "Sample Tool",
        "description": "A sample tool for testing",
        "category": "test",
        "function_name": "sample_function",
        "parameters": [
            {
                "name": "param1",
                "type": "integer",
                "description": "First parameter"
            }
        ],
        "gateway_tool_name": "tool-test",
        "endpoint": "http://test:8000"
    }


@pytest.fixture(scope="session")
def sample_model():
    """示例模型元数据"""
    return {
        "resource_id": "model:sample_model",
        "resource_type": "model",
        "name": "Sample Model",
        "description": "A sample model for testing",
        "input_type": "image",
        "output_type": "json",
        "gateway_tool_name": "sample_model",
        "endpoint": "http://test:8000",
        "gpu_memory_mb": 400
    }


@pytest.fixture(scope="session")
def sample_skill():
    """示例技能元数据"""
    return {
        "resource_id": "skill:sample_skill",
        "resource_type": "skill",
        "name": "Sample Skill",
        "description": "A sample skill for testing",
        "skill_type": "document_only",
        "skill_md_path": "tests/fixtures/sample_skill.md"
    }
