# Phase 4: 数据导入 + Docker 部署

## 概述

Phase 4 完成了完整的数据导入流程和 Docker 部署配置，使 MToolHub 能够与已有 Gateway 服务集成，形成完整的医疗工具智能调度平台。

---

## 新增文件

### 1. `scripts/import_from_gateway.py`
**功能：** 从 Gateway 的 `/tools` 接口导入所有工具和模型

**工作流程：**
1. 调用 `GET http://gateway:9000/tools` 获取所有已注册资源
2. 识别资源类型：
   - `type=remote, input=json` → 工具（tool-mdcalc / tool-unit / tool-scale）
   - `type=remote, input=image` → 模型（mavl）
3. 对于工具，进一步调用 `/tools/{name}/info` 获取详细信息（函数列表、参数定义等）
4. 解析并转换为注册表格式
5. 生成 `data/registry/tools.json` 和 `data/registry/models.json`

**使用方式：**
```bash
cd MToolHub/backend
python scripts/import_from_gateway.py [gateway_url] [output_dir]

# 默认参数
# gateway_url = http://localhost:9000
# output_dir = data/registry
```

**输出示例：**
```
🔍 正在从 Gateway 导入资源...
   Gateway URL: http://localhost:9000
✅ 发现 4 个已注册资源

📦 处理: tool-mdcalc
   类型: remote
   输入: json
   ✅ 导入 871 个函数

📦 处理: tool-unit
   类型: remote
   输入: json
   ✅ 导入 237 个函数

📦 处理: mavl
   类型: remote
   输入: image
   ✅ 导入模型

💾 已保存 1108 个工具到: data/registry/tools.json
💾 已保存 1 个模型到: data/registry/models.json

✨ 导入完成！
```

---

### 2. `scripts/import_skills.py`
**功能：** 从 `skills/` 目录扫描并导入所有技能

**技能类型检测规则：**
- **document_only**: 仅包含 `SKILL.md`
- **tool_reference**: `SKILL.md` + `references/` 目录
- **executable**: `SKILL.md` + `coworker.py`（包含 TOOLS 或函数定义）
- **complex_workflow**: `SKILL.md` + 大型数据/多个子目录

**元数据提取：**
- 从 `SKILL.md` 第一个 `#` 标题提取名称
- 从第一段文本提取描述
- 从 `Keywords:` 或 `关键词:` 行提取关键词
- 自动检测中英文

**使用方式：**
```bash
cd MToolHub/backend
python scripts/import_skills.py [skills_dir] [output_dir]

# 默认参数
# skills_dir = ../skills
# output_dir = data/registry
```

**输出示例：**
```
🔍 正在扫描 Skills 目录: ../skills
✅ 发现 88 个技能目录

📦 处理: clinical-report-writing
   类型: document_only
   ✅ 导入成功

📦 处理: care-coordination
   类型: tool_reference
   ✅ 导入成功

📦 处理: drug-interaction-check
   类型: executable
   ✅ 导入成功

💾 已保存 88 个技能到: data/registry/skills.json

📊 技能类型统计:
   document_only: 45
   tool_reference: 28
   executable: 12
   complex_workflow: 3

✨ 导入完成！
```

---

### 3. `Dockerfile`
**功能：** MToolHub 后端服务的 Docker 镜像

**关键特性：**
- 基于 `python:3.10-slim`
- 预下载 Embedding 模型（`pritamdeka/S-PubMedBert-MS-MARCO`）加速首次启动
- 健康检查：每 30 秒检查 `/api/health` 端点
- 暴露端口 8080

**构建命令：**
```bash
cd MToolHub/backend
docker build -t mtoolhub:latest .
```

---

### 4. `docker-compose.yml`（根目录）
**功能：** 整合 Gateway + MToolHub + 所有工具/模型服务

**服务列表：**
- **mtoolhub**: MToolHub 后端（端口 8080）
- **gateway**: Gateway 服务（端口 9000）
- **tool-mdcalc**: MDCalc 计算器（871 个工具）
- **tool-unit**: 单位换算（237 个工具）
- **tool-scale**: 评分工具（44 个，当前注释禁用）
- **mavl**: MAVL 胸片分析模型（GPU）

**网络配置：**
- 所有服务加入 `toolnet` 桥接网络
- 工具/模型服务仅 `expose` 端口（不对外暴露）
- Gateway 和 MToolHub 通过 `ports` 对外暴露

**环境变量：**
- `CLAUDE_API_KEY`: 从宿主机环境变量读取
- `GATEWAY_BASE_URL`: 容器内网地址 `http://gateway:9000`
- `EMBEDDING_MODEL`: 医学领域 Embedding 模型

---

## 完整部署流程

### 步骤 1: 准备环境变量
```bash
# 在项目根目录创建 .env 文件
cat > .env << EOF
CLAUDE_API_KEY=your_claude_api_key_here
EOF
```

### 步骤 2: 导入数据
```bash
# 确保 Gateway 服务正在运行
docker compose up -d gateway tool-mdcalc tool-unit mavl

# 等待服务启动（约 30 秒）
sleep 30

# 导入工具和模型
cd MToolHub/backend
python scripts/import_from_gateway.py

# 导入技能
python scripts/import_skills.py

# 构建 FAISS 索引
python scripts/build_index.py
```

**预期输出：**
```
✅ 已导入 1108 个工具
✅ 已导入 1 个模型
✅ 已导入 88 个技能
✅ 已构建 3 个 FAISS 索引（总计 1197 条记录）
```

### 步骤 3: 启动完整服务
```bash
# 返回项目根目录
cd ../..

# 构建并启动所有服务
docker compose up -d

# 查看日志
docker compose logs -f mtoolhub
```

### 步骤 4: 验证部署
```bash
# 1. 检查服务健康状态
curl http://localhost:8080/api/health
# 预期输出: {"status": "healthy", "version": "1.0.0"}

# 2. 查看资源统计
curl http://localhost:8080/api/tools | jq '.count'
# 预期输出: 1197

# 3. 测试语义搜索
curl "http://localhost:8080/api/tools/search?q=Wells+DVT&top_k=3" | jq
```

---

## 端到端测试

### 测试 1: 工具调用（MDCalc）
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "帮我计算 Wells DVT 评分，患者有活动性癌症，最近卧床3天，小腿有压痛"
  }' | jq
```

**预期响应：**
```json
{
  "response": "根据您提供的信息，Wells DVT 评分为 3 分...",
  "tools_used": ["tool-mdcalc:wells_score_dvt"],
  "routing_info": {
    "mode": "direct_call",
    "confidence": 0.92,
    "candidates": ["Wells Score for DVT"]
  }
}
```

### 测试 2: 模型调用（MAVL）
```bash
curl -X POST http://localhost:8080/api/chat \
  -F "message=分析这张胸片" \
  -F "file=@chest_xray.jpg" | jq
```

**预期响应：**
```json
{
  "response": "胸片分析结果显示：\n- 胸腔积液（Effusion）: 85%\n- 肺炎（Pneumonia）: 12%...",
  "tools_used": ["model:mavl"],
  "routing_info": {
    "mode": "direct_call",
    "confidence": 0.95
  }
}
```

### 测试 3: 技能调用（Care Coordination）
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "患者发来消息说胸痛，如何分诊？"
  }' | jq
```

**预期响应：**
```json
{
  "response": "根据患者主诉胸痛，建议按以下流程分诊：\n1. 立即评估生命体征...",
  "tools_used": ["skill:care-coordination"],
  "routing_info": {
    "mode": "claude_select",
    "confidence": 0.78
  }
}
```

### 测试 4: 直接执行接口
```bash
curl -X POST http://localhost:8080/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "resource_id": "tool-mdcalc:cha2ds2_vasc_score",
    "arguments": {
      "age": 75,
      "sex": "female",
      "chf": 1,
      "hypertension": 1,
      "stroke_tia": 0,
      "vascular_disease": 0,
      "diabetes": 0
    },
    "context": "评估房颤患者卒中风险"
  }' | jq
```

---

## 性能指标

### 预期性能
- **FAISS 检索延迟**: < 50ms（1197 条记录）
- **工具调用端到端**: < 2s（不含 Claude API）
- **对话接口端到端**: < 5s（含 Claude API）
- **Embedding 模型加载**: ~10s（首次启动）
- **MAVL 模型加载**: ~20-30s（首次调用）

### 资源占用
- **MToolHub 容器**: ~500MB 内存（含 Embedding 模型）
- **Gateway 容器**: ~100MB 内存
- **工具容器**: ~50MB 内存/容器
- **MAVL 容器**: ~400MB GPU 显存 + ~200MB 内存

---

## 故障排查

### 问题 1: MToolHub 启动失败
**症状：** `docker compose logs mtoolhub` 显示 `ModuleNotFoundError`

**解决：**
```bash
# 重新构建镜像
docker compose build mtoolhub
docker compose up -d mtoolhub
```

### 问题 2: 无法连接到 Gateway
**症状：** `/api/chat` 返回 `500 Internal Server Error`，日志显示 `Connection refused`

**解决：**
```bash
# 检查 Gateway 是否运行
docker compose ps gateway

# 检查网络连接
docker compose exec mtoolhub ping gateway

# 重启 Gateway
docker compose restart gateway
```

### 问题 3: FAISS 索引未找到
**症状：** `/api/tools/search` 返回 `404 Not Found`

**解决：**
```bash
# 重新构建索引
cd MToolHub/backend
python scripts/build_index.py

# 重启 MToolHub
docker compose restart mtoolhub
```

### 问题 4: Claude API 调用失败
**症状：** 对话接口返回 `Authentication error`

**解决：**
```bash
# 检查环境变量
docker compose exec mtoolhub env | grep CLAUDE_API_KEY

# 更新 .env 文件并重启
docker compose down
docker compose up -d
```

---

## 维护操作

### 更新工具注册表
```bash
# 1. 在 Gateway 添加新工具的 config.yaml
# 2. 重启 Gateway
docker compose restart gateway

# 3. 重新导入
cd MToolHub/backend
python scripts/import_from_gateway.py

# 4. 重建索引
python scripts/build_index.py

# 5. 重启 MToolHub
docker compose restart mtoolhub
```

### 更新技能
```bash
# 1. 在 skills/ 目录添加新技能
# 2. 重新导入
cd MToolHub/backend
python scripts/import_skills.py

# 3. 重建索引
python scripts/build_index.py

# 4. 重启 MToolHub
docker compose restart mtoolhub
```

### 查看日志
```bash
# 所有服务
docker compose logs -f

# 特定服务
docker compose logs -f mtoolhub
docker compose logs -f gateway
docker compose logs -f mavl
```

### 清理和重建
```bash
# 停止所有服务
docker compose down

# 清理数据（谨慎！）
rm -rf MToolHub/backend/data/registry/*.json
rm -rf MToolHub/backend/data/indexes/*

# 重新导入和构建
cd MToolHub/backend
python scripts/import_from_gateway.py
python scripts/import_skills.py
python scripts/build_index.py

# 重新启动
cd ../..
docker compose up -d
```

---

## 下一步优化方向

1. **会话管理**: 引入 Redis 持久化对话历史
2. **结果缓存**: 相同参数的工具调用结果缓存 1 小时
3. **监控告警**: Prometheus + Grafana 监控 API 调用
4. **前端界面**: React + TailwindCSS 对话式 UI
5. **权限管理**: JWT 认证 + RBAC 权限控制
6. **多语言支持**: 中英文查询自动识别和切换

---

## Phase 4 完成清单

- [x] `scripts/import_from_gateway.py` - 从 Gateway 导入工具和模型
- [x] `scripts/import_skills.py` - 从 skills/ 导入技能
- [x] `Dockerfile` - MToolHub 容器镜像
- [x] `docker-compose.yml` - 完整服务编排
- [x] `.dockerignore` - Docker 构建排除规则
- [x] `README_PHASE4.md` - 部署和测试文档

**状态：** ✅ Phase 4 完成
