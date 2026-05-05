#!/bin/bash

# MToolHub 快速启动脚本
# 用途：自动化完成数据导入、索引构建和服务启动

set -e  # 遇到错误立即退出

echo "🚀 MToolHub 快速启动脚本"
echo "========================"
echo ""

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "❌ 未找到 .env 文件"
    echo "请创建 .env 文件并设置 CLAUDE_API_KEY"
    echo ""
    echo "示例："
    echo "  cat > .env << EOF"
    echo "  CLAUDE_API_KEY=your_api_key_here"
    echo "  EOF"
    exit 1
fi

echo "✅ 找到 .env 文件"
echo ""

# 步骤 1: 启动基础服务
echo "📦 步骤 1/5: 启动 Gateway 和工具服务..."
docker compose up -d gateway tool-mdcalc tool-unit mavl

echo "⏳ 等待服务启动（30 秒）..."
sleep 30

# 检查 Gateway 健康状态
echo "🔍 检查 Gateway 状态..."
if curl -s http://localhost:9000/tools > /dev/null; then
    echo "✅ Gateway 运行正常"
else
    echo "❌ Gateway 未响应，请检查日志："
    echo "   docker compose logs gateway"
    exit 1
fi
echo ""

# 步骤 2: 导入工具和模型
echo "📥 步骤 2/5: 从 Gateway 导入工具和模型..."
cd MToolHub/backend
python scripts/import_from_gateway.py

if [ ! -f data/registry/tools.json ]; then
    echo "❌ 工具导入失败"
    exit 1
fi
echo "✅ 工具和模型导入完成"
echo ""

# 步骤 3: 导入技能
echo "📥 步骤 3/5: 导入技能..."
python scripts/import_skills.py

if [ ! -f data/registry/skills.json ]; then
    echo "❌ 技能导入失败"
    exit 1
fi
echo "✅ 技能导入完成"
echo ""

# 步骤 4: 构建 FAISS 索引
echo "🔨 步骤 4/5: 构建 FAISS 索引..."
python scripts/build_index.py

if [ ! -f data/indexes/faiss.index ]; then
    echo "❌ 索引构建失败"
    exit 1
fi
echo "✅ FAISS 索引构建完成"
echo ""

# 返回项目根目录
cd ../..

# 步骤 5: 启动 MToolHub
echo "🚀 步骤 5/5: 启动 MToolHub 服务..."
docker compose up -d mtoolhub

echo "⏳ 等待 MToolHub 启动（20 秒）..."
sleep 20

# 验证部署
echo ""
echo "🔍 验证部署..."

# 检查健康状态
if curl -s http://localhost:8080/api/health | grep -q "healthy"; then
    echo "✅ MToolHub 健康检查通过"
else
    echo "❌ MToolHub 健康检查失败"
    echo "查看日志："
    echo "   docker compose logs mtoolhub"
    exit 1
fi

# 检查资源数量
RESOURCE_COUNT=$(curl -s http://localhost:8080/api/tools | grep -o '"count":[0-9]*' | grep -o '[0-9]*')
echo "✅ 已加载 $RESOURCE_COUNT 个资源"

echo ""
echo "========================"
echo "✨ MToolHub 启动完成！"
echo ""
echo "📍 服务地址："
echo "   - MToolHub API: http://localhost:8080"
echo "   - API 文档: http://localhost:8080/docs"
echo "   - Gateway: http://localhost:9000"
echo ""
echo "🧪 快速测试："
echo '   curl -X POST http://localhost:8080/api/chat \'
echo '     -H "Content-Type: application/json" \'
echo '     -d '"'"'{"message": "帮我计算 Wells DVT 评分"}'"'"
echo ""
echo "📚 查看文档："
echo "   cat MToolHub/README.md"
echo ""
echo "📊 查看日志："
echo "   docker compose logs -f mtoolhub"
echo ""
