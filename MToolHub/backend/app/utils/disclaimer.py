"""
医疗免责声明工具
"""

from app.config import settings


def get_disclaimer() -> str:
    """获取医疗免责声明"""
    return settings.medical_disclaimer


def add_disclaimer_to_response(response: str) -> str:
    """在响应中添加免责声明"""
    return f"{response}\n\n⚠️ {get_disclaimer()}"
