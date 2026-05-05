"""
构建 FAISS 索引脚本

从注册表 JSON 文件读取资源，生成向量并构建 FAISS 索引
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.registry import registry_manager
from app.core.faiss_index import FAISSIndex
from app.core.embedding import embedding_model


def build_index_for_category(category: str, items: list):
    """
    为指定类别构建索引

    Args:
        category: 类别名称（tool/model/skill）
        items: 资源列表
    """
    print(f"\n{'='*60}")
    print(f"构建 {category} 索引")
    print(f"{'='*60}")

    if not items:
        print(f"警告：{category} 类别没有资源，跳过")
        return

    # 转换为字典格式
    items_dict = [item.model_dump() for item in items]

    # 创建索引
    index = FAISSIndex(category)
    index.build(items_dict)
    index.save()


def main():
    """主函数"""
    print("="*60)
    print("FAISS 索引构建工具")
    print("="*60)

    # 确保 Embedding 模型已加载
    print(f"\n向量维度：{embedding_model.dimension}")

    # 构建三类索引
    build_index_for_category("tool", registry_manager.tools)
    build_index_for_category("model", registry_manager.models)
    build_index_for_category("skill", registry_manager.skills)

    print("\n" + "="*60)
    print("✓ 所有索引构建完成")
    print("="*60)


if __name__ == "__main__":
    main()
