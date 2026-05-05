"""
executor.py — 通过 exec() 动态执行工具代码。
"""
from __future__ import annotations

from typing import Any, Dict


def run_tool(tool: Dict[str, Any], arguments: Dict[str, Any]) -> Any:
    """
    执行工具函数。

    arguments 支持两种格式：
      - 纯值：{"age": 65, "spo2": 94}
      - LLM 输出格式：{"age": {"Value": 65, "Unit": "years"}, ...}
    两种格式自动识别，统一展开为纯值后传入函数。
    """
    # 展开 Value/Unit 格式
    flat: Dict[str, Any] = {}
    for k, v in arguments.items():
        if isinstance(v, dict) and "Value" in v:
            flat[k] = v["Value"]
        else:
            flat[k] = v

    local_ns: Dict[str, Any] = {}
    exec(tool["code"], {}, local_ns)  # noqa: S102
    func = local_ns[tool["function_name"]]
    return func(**flat)
