"""
配置管理模块

使用 pydantic-settings 管理所有配置项，支持从环境变量和 .env 文件加载
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""

    # 服务配置
    app_name: str = "MToolHub"
    app_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = False

    # Gateway 配置
    gateway_base_url: str = "http://localhost:9000"
    gateway_timeout: int = 60

    # Claude API
    claude_api_key: str
    claude_model: str = "claude-sonnet-4-20250514"
    claude_max_tokens: int = 4096

    # Embedding 模型
    embedding_model: str = "pritamdeka/S-PubMedBert-MS-MARCO"
    embedding_device: str = "cpu"
    embedding_cache_dir: Optional[str] = None

    # FAISS 索引路径
    faiss_index_dir: str = "data/indexes"

    # 路由阈值
    direct_call_threshold: float = 0.85
    claude_select_threshold: float = 0.60

    # 注册表路径
    registry_dir: str = "data/registry"
    tools_registry_path: str = "data/registry/tools.json"
    models_registry_path: str = "data/registry/models.json"
    skills_registry_path: str = "data/registry/skills.json"

    # Skills 目录（相对于项目根目录）
    skills_dir: str = "../skills"

    # 医疗免责声明
    medical_disclaimer: str = "本系统提供的信息仅供参考，不构成医疗建议。请咨询专业医疗人员进行诊断和治疗。"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 全局配置实例
settings = Settings()
