"""
state.py — 全局可变状态（替代 singleton，避免循环导入）。
"""
from __future__ import annotations

from typing import Any, Dict

app_state: Dict[str, Any] = {
    "registry": None,
    "loaded": False,
}
