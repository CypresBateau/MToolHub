"""
FastAPI 主应用入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import tools, health, search, chat, execute

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="医疗工具智能调度平台 - 统一的语义路由层",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health.router, tags=["健康检查"])
app.include_router(tools.router, tags=["工具管理"])
app.include_router(search.router, tags=["语义搜索"])
app.include_router(chat.router, tags=["对话接口"])
app.include_router(execute.router, tags=["直接执行"])


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print(f"🚀 {settings.app_name} v{settings.app_version} 启动中...")
    print(f"📍 Gateway: {settings.gateway_base_url}")
    print(f"🤖 Claude Model: {settings.claude_model}")
    print(f"🔍 Embedding Model: {settings.embedding_model}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print(f"👋 {settings.app_name} 已关闭")


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
