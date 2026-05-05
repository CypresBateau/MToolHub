"""
tool_registry.py — 从 tools_metadata.json 加载工具列表，按 function_name 索引。
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional


class ToolRegistry:
    CATEGORY = "mdcalc"

    def __init__(self) -> None:
        self._tools: Dict[str, Dict[str, Any]] = {}

    def load(self, json_path: str) -> None:
        with open(json_path, "r", encoding="utf-8") as f:
            tools: List[Dict[str, Any]] = json.load(f)

        for tool in tools:
            fn = tool.get("function_name")
            if fn:
                self._tools[fn] = tool

        print(f"[ToolRegistry] Loaded {len(self._tools)} tools from {json_path}")

    @property
    def category(self) -> str:
        return self.CATEGORY

    def get(self, function_name: str) -> Optional[Dict[str, Any]]:
        return self._tools.get(function_name)

    def all(self) -> Dict[str, Dict[str, Any]]:
        return dict(self._tools)

    def count(self) -> int:
        return len(self._tools)
