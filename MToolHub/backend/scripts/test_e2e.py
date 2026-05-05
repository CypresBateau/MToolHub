"""
MToolHub 端到端测试脚本

运行方式：
    python scripts/test_e2e.py

功能：
    1. 测试健康检查
    2. 测试资源列表和搜索
    3. 测试工具调用（MDCalc）
    4. 测试直接执行接口
    5. 测试对话接口
"""

import asyncio
import httpx
import json
from typing import Dict, Any


BASE_URL = "http://localhost:8080"
TIMEOUT = 30.0


class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_test(name: str):
    """打印测试名称"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}测试: {name}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")


def print_success(message: str):
    """打印成功消息"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")


def print_error(message: str):
    """打印错误消息"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")


def print_info(message: str):
    """打印信息"""
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.END}")


async def test_health_check():
    """测试健康检查"""
    print_test("健康检查")

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            resp = await client.get(f"{BASE_URL}/api/health")
            resp.raise_for_status()
            data = resp.json()

            if data.get("status") == "healthy":
                print_success(f"服务健康，版本: {data.get('version')}")
                return True
            else:
                print_error(f"服务状态异常: {data}")
                return False
        except Exception as e:
            print_error(f"健康检查失败: {e}")
            return False


async def test_resource_list():
    """测试资源列表"""
    print_test("资源列表")

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            resp = await client.get(f"{BASE_URL}/api/tools?limit=10")
            resp.raise_for_status()
            data = resp.json()

            count = data.get("count", 0)
            items = data.get("items", [])

            print_success(f"总资源数: {count}")
            print_info(f"前 {len(items)} 个资源:")
            for item in items[:3]:
                print(f"  - {item['name']} ({item['resource_id']})")

            return count > 0
        except Exception as e:
            print_error(f"获取资源列表失败: {e}")
            return False


async def test_semantic_search():
    """测试语义搜索"""
    print_test("语义搜索")

    queries = [
        "Wells DVT",
        "深静脉血栓",
        "胸片分析",
        "血糖单位换算"
    ]

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        success_count = 0

        for query in queries:
            try:
                resp = await client.get(
                    f"{BASE_URL}/api/tools/search",
                    params={"q": query, "top_k": 3}
                )
                resp.raise_for_status()
                data = resp.json()

                results = data.get("results", [])
                if results:
                    print_success(f"查询 '{query}' 找到 {len(results)} 个结果")
                    print_info(f"  最佳匹配: {results[0]['name']} (score: {results[0]['score']:.3f})")
                    success_count += 1
                else:
                    print_error(f"查询 '{query}' 无结果")
            except Exception as e:
                print_error(f"查询 '{query}' 失败: {e}")

        return success_count == len(queries)


async def test_direct_execute():
    """测试直接执行接口"""
    print_test("直接执行接口")

    # 测试 CHA2DS2-VASc 评分
    request_data = {
        "resource_id": "tool-mdcalc:cha2ds2_vasc_score",
        "arguments": {
            "age": 75,
            "sex": "female",
            "chf": 1,
            "hypertension": 1,
            "stroke_tia": 0,
            "vascular_disease": 0,
            "diabetes": 0
        },
        "context": "评估房颤患者卒中风险"
    }

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            resp = await client.post(
                f"{BASE_URL}/api/execute",
                json=request_data
            )
            resp.raise_for_status()
            data = resp.json()

            if data.get("success"):
                print_success("执行成功")
                print_info(f"结果: {json.dumps(data.get('result'), ensure_ascii=False, indent=2)}")
                return True
            else:
                print_error(f"执行失败: {data}")
                return False
        except Exception as e:
            print_error(f"直接执行失败: {e}")
            return False


async def test_chat_interface():
    """测试对话接口"""
    print_test("对话接口")

    test_cases = [
        {
            "name": "工具调用 - Wells DVT",
            "message": "帮我计算 Wells DVT 评分，患者有活动性癌症"
        },
        {
            "name": "单位换算",
            "message": "100 mg/dL 的血糖是多少 mmol/L？"
        },
        {
            "name": "纯对话",
            "message": "什么是深静脉血栓？"
        }
    ]

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        success_count = 0

        for case in test_cases:
            print_info(f"\n测试用例: {case['name']}")

            try:
                resp = await client.post(
                    f"{BASE_URL}/api/chat",
                    json={"message": case["message"]}
                )
                resp.raise_for_status()
                data = resp.json()

                response = data.get("response", "")
                routing_info = data.get("routing_info", {})
                tools_used = data.get("tools_used", [])

                print_success(f"路由模式: {routing_info.get('mode')}")
                print_info(f"置信度: {routing_info.get('confidence', 0):.3f}")
                if tools_used:
                    print_info(f"使用工具: {', '.join(tools_used)}")
                print_info(f"回复: {response[:100]}...")

                success_count += 1
            except Exception as e:
                print_error(f"测试失败: {e}")

        return success_count == len(test_cases)


async def test_resource_detail():
    """测试资源详情"""
    print_test("资源详情")

    resource_ids = [
        "tool-mdcalc:wells_score_dvt",
        "model:mavl",
        "skill:clinical-report-writing"
    ]

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        success_count = 0

        for resource_id in resource_ids:
            try:
                resp = await client.get(f"{BASE_URL}/api/tools/{resource_id}")
                resp.raise_for_status()
                data = resp.json()

                print_success(f"资源: {data.get('name')}")
                print_info(f"  类型: {data.get('resource_type')}")
                print_info(f"  描述: {data.get('description', '')[:50]}...")
                success_count += 1
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    print_error(f"资源不存在: {resource_id}")
                else:
                    print_error(f"获取失败: {e}")
            except Exception as e:
                print_error(f"获取失败: {e}")

        return success_count > 0


async def run_all_tests():
    """运行所有测试"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}MToolHub 端到端测试{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

    tests = [
        ("健康检查", test_health_check),
        ("资源列表", test_resource_list),
        ("语义搜索", test_semantic_search),
        ("资源详情", test_resource_detail),
        ("直接执行", test_direct_execute),
        ("对话接口", test_chat_interface),
    ]

    results = []

    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"测试 '{name}' 异常: {e}")
            results.append((name, False))

    # 打印总结
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}测试总结{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = f"{Colors.GREEN}✅ 通过{Colors.END}" if result else f"{Colors.RED}❌ 失败{Colors.END}"
        print(f"{name}: {status}")

    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print(f"\n{Colors.GREEN}🎉 所有测试通过！{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}⚠️  部分测试失败{Colors.END}")
        return 1


if __name__ == "__main__":
    import sys

    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
