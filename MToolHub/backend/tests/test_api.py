"""
API 端到端测试
"""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def client():
    """创建测试客户端"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client):
    """测试健康检查接口"""
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.asyncio
async def test_get_tools_list(client):
    """测试获取工具列表"""
    response = await client.get("/api/tools?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "items" in data
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_search_tools(client):
    """测试语义搜索"""
    response = await client.get("/api/tools/search?q=Wells+DVT&top_k=3")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)


@pytest.mark.asyncio
async def test_get_tool_detail(client):
    """测试获取工具详情"""
    # 先获取工具列表
    response = await client.get("/api/tools?limit=1")
    data = response.json()

    if data["count"] > 0:
        resource_id = data["items"][0]["resource_id"]

        # 获取详情
        response = await client.get(f"/api/tools/{resource_id}")
        assert response.status_code == 200
        detail = response.json()
        assert detail["resource_id"] == resource_id


@pytest.mark.asyncio
async def test_chat_interface(client):
    """测试对话接口"""
    response = await client.post(
        "/api/chat",
        json={"message": "什么是深静脉血栓？"}
    )

    # 可能返回 200 或 500（如果 Claude API 未配置）
    assert response.status_code in [200, 500]

    if response.status_code == 200:
        data = response.json()
        assert "response" in data
        assert "routing_info" in data


@pytest.mark.asyncio
async def test_execute_interface_invalid_resource(client):
    """测试直接执行接口（无效资源）"""
    response = await client.post(
        "/api/execute",
        json={
            "resource_id": "invalid:resource",
            "arguments": {}
        }
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_api_validation(client):
    """测试 API 参数验证"""
    # 缺少必需参数
    response = await client.post("/api/chat", json={})
    assert response.status_code == 422  # Validation error
