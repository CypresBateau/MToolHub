"""
从 Gateway 导入工具和模型到注册表

运行方式：
    python scripts/import_from_gateway.py

功能：
    1. 调用 Gateway 的 GET /tools 接口获取所有已注册资源
    2. 解析工具类型（tool-mdcalc, tool-unit, tool-scale）和模型（mavl）
    3. 对于工具，进一步调用 /tools/{name}/info 获取详细信息
    4. 生成 tools.json 和 models.json 注册表文件
"""

import asyncio
import httpx
import json
from pathlib import Path
from typing import Dict, List, Any


async def fetch_gateway_tools(gateway_url: str) -> Dict[str, Any]:
    """获取 Gateway 所有已注册工具"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.get(f"{gateway_url}/tools")
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"❌ 无法连接到 Gateway: {e}")
            return {}


async def fetch_tool_functions(endpoint: str) -> List[Dict[str, Any]]:
    """直接调用工具容器的 /api/v1/tools 接口获取函数列表"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.get(f"{endpoint}/api/v1/tools")
            resp.raise_for_status()
            data = resp.json()
            return data.get("tools", [])
        except Exception as e:
            print(f"⚠️  无法获取工具函数列表: {e}")
            return []


def parse_tool_metadata(name: str, info: Dict[str, Any], functions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """解析工具元数据为注册表格式"""
    # 确定类别
    if "mdcalc" in name:
        category = "mdcalc"
    elif "unit" in name:
        category = "unit"
    elif "scale" in name:
        category = "scale"
    else:
        category = "other"

    tools = []
    for func in functions:
        resource_id = f"{name}:{func['function_name']}"
        tool = {
            "resource_id": resource_id,
            "resource_type": "tool",
            "name": func.get("tool_name", func["function_name"]),
            "name_zh": None,
            "description": func.get("short_description", ""),
            "description_zh": None,
            "keywords": [],
            "category": category,
            "function_name": func["function_name"],
            "parameters": [],   # 详细参数需要调用 /api/v1/tools/{function_name}
            "gateway_tool_name": name,
            "endpoint": info.get("endpoint", "")
        }
        tools.append(tool)

    return tools


def parse_model_metadata(name: str, info: Dict[str, Any]) -> Dict[str, Any]:
    """解析模型元数据为注册表格式"""
    return {
        "resource_id": f"model:{name}",
        "resource_type": "model",
        "name": info.get("description", name),
        "name_zh": info.get("description_zh"),
        "description": info.get("description", ""),
        "description_zh": info.get("description_zh"),
        "keywords": info.get("keywords", []),
        "input_type": info.get("input", "image"),
        "output_type": info.get("output", "json"),
        "gateway_tool_name": name,
        "endpoint": f"http://{name}:8000",
        "gpu_memory_mb": info.get("gpu_memory_mb", 0)
    }


async def import_from_gateway(gateway_url: str, output_dir: str):
    """主导入流程"""
    print(f"🔍 正在从 Gateway 导入资源...")
    print(f"   Gateway URL: {gateway_url}")

    # 1. 获取所有工具列表
    tools_data = await fetch_gateway_tools(gateway_url)
    if not tools_data:
        print("❌ 未能获取任何工具数据")
        return

    print(f"✅ 发现 {len(tools_data)} 个已注册资源")

    # 2. 分类处理
    all_tools = []
    all_models = []

    for name, info in tools_data.items():
        print(f"\n📦 处理: {name}")
        print(f"   类型: {info.get('type')}")
        print(f"   输入: {info.get('input')}")

        if info.get("type") == "remote":
            if info.get("input") == "json":
                # 这是工具（MDCalc / Unit / Scale）
                endpoint = f"http://{name}:8000"
                functions = await fetch_tool_functions(endpoint)
                if functions:
                    tools = parse_tool_metadata(name, info, functions)
                    all_tools.extend(tools)
                    print(f"   ✅ 导入 {len(tools)} 个函数")

            elif info.get("input") == "image":
                # 这是模型（MAVL）
                model = parse_model_metadata(name, info)
                all_models.append(model)
                print(f"   ✅ 导入模型")

    # 3. 保存到 JSON
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    tools_file = output_path / "tools.json"
    with open(tools_file, "w", encoding="utf-8") as f:
        json.dump(all_tools, f, ensure_ascii=False, indent=2)
    print(f"\n💾 已保存 {len(all_tools)} 个工具到: {tools_file}")

    models_file = output_path / "models.json"
    with open(models_file, "w", encoding="utf-8") as f:
        json.dump(all_models, f, ensure_ascii=False, indent=2)
    print(f"💾 已保存 {len(all_models)} 个模型到: {models_file}")

    print("\n✨ 导入完成！")


if __name__ == "__main__":
    import sys

    # 默认配置
    GATEWAY_URL = "http://localhost:9000"
    OUTPUT_DIR = "data/registry"

    # 支持命令行参数
    if len(sys.argv) > 1:
        GATEWAY_URL = sys.argv[1]
    if len(sys.argv) > 2:
        OUTPUT_DIR = sys.argv[2]

    asyncio.run(import_from_gateway(GATEWAY_URL, OUTPUT_DIR))
