"""
健康检查路由
"""

from fastapi import APIRouter
from app.config import settings
from app.core.registry import registry_manager

router = APIRouter()


@router.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "resources": {
            "tools": len(registry_manager.tools),
            "models": len(registry_manager.models),
            "skills": len(registry_manager.skills),
        },
    }
