# FAISS 索引目录

此目录用于存储 FAISS 向量索引文件。

## 文件说明

运行 `python scripts/build_index.py` 后，此目录将包含：

- `faiss.index` - FAISS 向量索引文件
- `metadata.json` - 索引元数据（资源 ID 映射）

## 首次使用

1. 确保已导入注册表数据：
   ```bash
   python scripts/import_from_gateway.py
   python scripts/import_skills.py
   ```

2. 构建索引：
   ```bash
   python scripts/build_index.py
   ```

3. 验证索引文件已生成：
   ```bash
   ls -lh data/indexes/
   ```

## 重建索引

当注册表数据更新后（添加新工具/模型/技能），需要重建索引：

```bash
python scripts/build_index.py
```

## 注意事项

- 索引文件较大（约 50-100MB），已添加到 `.gitignore`
- 首次启动前必须构建索引，否则语义搜索功能无法使用
- 索引构建时间约 30-60 秒（取决于资源数量）
