"""
registry.py — 扫描 tools/*/config.yaml，自动注册所有工具。
新增工具只需在 tools/ 下新建文件夹并放入 config.yaml，无需修改任何代码。
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Dict[str, Any]] = {}

    def scan(self, tools_dir: Optional[str] = None) -> None:
        """扫描工具目录，注册所有 config.yaml。"""
        if tools_dir is None:
            tools_dir = str(Path(__file__).parent.parent / "tools")

        for config_file in sorted(Path(tools_dir).glob("*/config.yaml")):
            try:
                with open(config_file) as f:
                    cfg = yaml.safe_load(f)
                name = cfg["name"]
                self._tools[name] = cfg
                print(f"[Registry] Registered: {name}  type={cfg.get('type')}  gpu={cfg.get('gpu_memory_mb', 0)}MB")
            except Exception as e:
                print(f"[Registry] Failed to load {config_file}: {e}")

        print(f"[Registry] Total tools: {len(self._tools)}")

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        return self._tools.get(name)

    def all(self) -> Dict[str, Dict[str, Any]]:
        return dict(self._tools)
