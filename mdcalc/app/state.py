"""
state.py — 全局可变状态，避免 main.py 与各 router 之间的循环导入。
"""
from __future__ import annotations

from typing import Any, Dict

app_state: Dict[str, Any] = {
    "registry": None,
    "loaded": False,
}
