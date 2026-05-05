"""
核心模块初始化
"""

from app.core.registry import RegistryManager, registry_manager
from app.core.embedding import EmbeddingModel, embedding_model
from app.core.faiss_index import FAISSIndex, VectorSearchEngine, vector_search_engine

__all__ = [
    "RegistryManager",
    "registry_manager",
    "EmbeddingModel",
    "embedding_model",
    "FAISSIndex",
    "VectorSearchEngine",
    "vector_search_engine",
]
