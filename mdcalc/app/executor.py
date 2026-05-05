"""
executor.py — 通过 exec() 动态执行工具代码。

与 med-calc executor 的关键区别：
  - 代码字段为 generated_code（而非 code）
  - generated_code 内含 import 语句，需传入 __builtins__ 保证 import 可用
  - 返回值统一为 dict
"""
from __future__ import annotations

from typing import Any, Dict


def run_tool(tool: Dict[str, Any], arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行工具函数。

    arguments 支持两种格式：
      - 纯值：{"weight": 70.0, "height": 175.0}
      - LLM 输出格式：{"weight": {"Value": 70.0, "Unit": "kg"}, ...}
    两种格式自动识别，统一展开为纯值后传入函数。
    """
    flat: Dict[str, Any] = {}
    for k, v in arguments.items():
        if isinstance(v, dict) and "Value" in v:
            flat[k] = v["Value"]
        else:
            flat[k] = v

    # generated_code 含顶层 import，需传入 __builtins__ 才能正常执行
    local_ns: Dict[str, Any] = {}
    exec(tool["generated_code"], {"__builtins__": __builtins__}, local_ns)  # noqa: S102
    func = local_ns[tool["function_name"]]
    return func(**flat)
