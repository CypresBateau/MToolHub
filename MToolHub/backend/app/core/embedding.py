"""
Embedding 模型管理

使用 sentence-transformers 加载医学领域的 Embedding 模型
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
from app.config import settings


class EmbeddingModel:
    """Embedding 模型单例"""

    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            self._load_model()

    def _load_model(self):
        """加载 Embedding 模型"""
        print(f"正在加载 Embedding 模型：{settings.embedding_model}")
        try:
            self._model = SentenceTransformer(
                settings.embedding_model,
                device=settings.embedding_device,
                cache_folder=settings.embedding_cache_dir,
            )
            print(f"✓ Embedding 模型加载成功")
        except Exception as e:
            print(f"✗ Embedding 模型加载失败：{e}")
            raise

    def encode(self, texts: Union[str, List[str]], normalize: bool = True) -> np.ndarray:
        """
        将文本编码为向量

        Args:
            texts: 单个文本或文本列表
            normalize: 是否归一化向量（用于余弦相似度）

        Returns:
            numpy 数组，shape 为 (n, dim) 或 (dim,)
        """
        if self._model is None:
            raise RuntimeError("Embedding 模型未加载")

        # 确保输入是列表
        is_single = isinstance(texts, str)
        if is_single:
            texts = [texts]

        # 编码
        embeddings = self._model.encode(
            texts,
            normalize_embeddings=normalize,
            show_progress_bar=False,
        )

        # 如果输入是单个文本，返回一维数组
        if is_single:
            return embeddings[0]

        return embeddings

    @property
    def dimension(self) -> int:
        """获取向量维度"""
        if self._model is None:
            raise RuntimeError("Embedding 模型未加载")
        return self._model.get_sentence_embedding_dimension()


# 全局 Embedding 模型实例
embedding_model = EmbeddingModel()
