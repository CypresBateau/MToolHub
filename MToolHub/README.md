# MToolHub - 医疗工具智能调度平台

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 项目简介

**MToolHub** 是一个医疗工具智能调度平台，在已有 Gateway 服务之上新增**语义路由层**，使用户能够通过**自然语言**查询和调用医疗资源。

### 核心功能

- 🔍 **语义检索**: 基于 FAISS + 医学领域 Embedding 模型的向量检索
- 🤖 **智能路由**: 三级置信度路由策略（直接调用 / Claude 选择 / 纯对话）
- 🛠️ **统一接口**: 整合 1200+ 医疗工具、AI 模型和技能
- 💬 **对话式交互**: 自然语言参数提取和结果解释
- 🚀 **高性能**: FAISS 检索 < 50ms，端到端响应 < 5s

### 管理的资源

| 类别 | 数量 | 说明 |
|------|------|------|
| **医疗计算工具** | 1108 | MDCalc 计算器（871）+ 单位换算（237）+ 评分工具（44，禁用） |
| **AI 模型** | 1 | MAVL 胸片分析模型（GPU，400MB 显存） |
| **医疗技能** | 88 | 基于 LLM 的医疗技能（含 prompt 模板和可选工具） |
| **总计** | 1197 | 统一语义检索和调用 |

---

## 架构设计

```
用户请求（自然语言）
    ↓
MToolHub Backend (FastAPI, 端口 8080)
    ├── API 层
    │   ├── POST /api/chat          # 对话接口
    │   ├── POST /api/execute       # 直接执行接口
    │   ├── GET /api/tools          # 工具列表
    │   └── GET /api/tools/search   # 语义搜索
    │
    ├── 路由层（Router）
    │   ├── FAISS 向量检索
    │   ├── 置信度评分
    │   └── 路由决策（3 种模式）
    │
    └── 执行层（Executor）
        ├── ToolExecutor    → Gateway /tools/{name}/call
        ├── ModelExecutor   → Gateway /tools/{name}/predict
        └── SkillExecutor   → Claude API（注入 SKILL.md）
            ↓
    Gateway (端口 9000)
        ↓
    tool-mdcalc / tool-unit / mavl 容器
```

### 路由策略

| 模式 | 触发条件 | 行为 |
|------|---------|------|
| `direct_call` | score ≥ 0.85 | 直接调用匹配资源；用 Claude 提取参数 + 解释结果 |
| `claude_select` | 0.60 ≤ score < 0.85 | 将 top-3 候选作为 tools 传给 Claude，由 Claude 选择 |
| `chat_only` | score < 0.60 | 纯 Claude 对话，不调用工具 |

---

## 快速开始

### 前置要求

- Docker 和 Docker Compose
- Python 3.10+（用于数据导入脚本）
- Claude API Key
- NVIDIA GPU（可选，用于 MAVL 模型）

### 步骤 1: 克隆项目

```bash
git clone <repository_url>
cd AgentHospital
```

### 步骤 2: 配置环境变量

```bash
# 创建 .env 文件
cat > .env << EOF
CLAUDE_API_KEY=your_claude_api_key_here
EOF
```

### 步骤 3: 导入数据

```bash
# 启动 Gateway 和工具服务
docker compose up -d gateway tool-mdcalc tool-unit mavl

# 等待服务启动
sleep 30

# 导入工具和模型
cd MToolHub/backend
python scripts/import_from_gateway.py

# 导入技能
python scripts/import_skills.py

# 构建 FAISS 索引
python scripts/build_index.py
```

### 步骤 4: 启动完整服务

```bash
# 返回项目根目录
cd ../..

# 启动所有服务
docker compose up -d

# 查看日志
docker compose logs -f mtoolhub
```

### 步骤 5: 验证部署

```bash
# 检查健康状态
curl http://localhost:8080/api/health

# 查看资源统计
curl http://localhost:8080/api/tools | jq '.count'
# 预期输出: 1197

# 测试语义搜索
curl "http://localhost:8080/api/tools/search?q=Wells+DVT&top_k=3" | jq
```

---

## API 使用示例

### 1. 对话接口（自然语言）

```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "帮我计算 Wells DVT 评分，患者有活动性癌症，最近卧床3天"
  }'
```

**响应：**
```json
{
  "response": "根据您提供的信息，Wells DVT 评分为 3 分，属于中度风险...",
  "tools_used": ["tool-mdcalc:wells_score_dvt"],
  "routing_info": {
    "mode": "direct_call",
    "confidence": 0.92
  }
}
```

### 2. 图像分析（胸片）

```bash
curl -X POST http://localhost:8080/api/chat \
  -F "message=分析这张胸片" \
  -F "file=@chest_xray.jpg"
```

### 3. 直接执行接口（已知资源 ID）

```bash
curl -X POST http://localhost:8080/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "resource_id": "tool-mdcalc:cha2ds2_vasc_score",
    "arguments": {
      "age": 75,
      "sex": "female",
      "chf": 1,
      "hypertension": 1
    }
  }'
```

### 4. 语义搜索

```bash
curl "http://localhost:8080/api/tools/search?q=深静脉血栓&top_k=5"
```

### 5. 浏览资源

```bash
# 获取所有资源
curl "http://localhost:8080/api/tools?limit=20&offset=0"

# 按类别筛选
curl "http://localhost:8080/api/tools?category=tool&limit=20"

# 获取单个资源详情
curl "http://localhost:8080/api/tools/tool-mdcalc:wells_score_dvt"
```

---

## 项目结构

```
AgentHospital/
├── MToolHub/                       # MToolHub 后端服务
│   └── backend/
│       ├── app/                    # 应用代码
│       │   ├── core/               # 核心组件（注册表、索引、Claude 客户端）
│       │   ├── models/             # 数据模型
│       │   ├── routers/            # API 路由
│       │   ├── services/           # 业务逻辑（路由、执行器）
│       │   ├── utils/              # 工具函数
│       │   ├── config.py           # 配置管理
│       │   └── main.py             # FastAPI 入口
│       ├── data/                   # 数据文件
│       │   ├── registry/           # 注册表 JSON
│       │   └── indexes/            # FAISS 索引
│       ├── scripts/                # 数据导入脚本
│       │   ├── import_from_gateway.py
│       │   ├── import_skills.py
│       │   └── build_index.py
│       ├── tests/                  # 测试
│       ├── Dockerfile              # Docker 镜像
│       ├── requirements.txt        # Python 依赖
│       └── README_PHASE*.md        # 各阶段文档
├── gateway/                        # Gateway 服务（已有）
├── mdcalc/                         # MDCalc 工具服务（已有）
├── med-calc/                       # 单位换算和评分工具（已有）
├── MAVL/                           # MAVL 胸片分析模型（已有）
├── skills/                         # 医疗技能目录（已有）
├── docker-compose.yml              # 服务编排
├── CLAUDE.md                       # Claude Code 指南
└── README.md                       # 本文件
```

---

## 技术栈

| 组件 | 技术选型 |
|------|---------|
| 后端框架 | FastAPI + uvicorn |
| 数据验证 | Pydantic v2 |
| 向量检索 | FAISS（faiss-cpu） |
| Embedding | sentence-transformers + S-PubMedBert-MS-MARCO |
| LLM | Claude API（claude-sonnet-4-20250514） |
| HTTP 客户端 | httpx（异步） |
| 容器化 | Docker + Docker Compose |

---

## 开发指南

### 本地开发

```bash
cd MToolHub/backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 CLAUDE_API_KEY

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### 运行测试

```bash
cd MToolHub/backend
pytest tests/ -v
```

### 添加新工具到 Gateway

1. 在 `gateway/tools/{name}/` 创建 `config.yaml`
2. 在 `docker-compose.yml` 添加服务定义
3. 重启 Gateway：`docker compose restart gateway`
4. 重新导入：`python scripts/import_from_gateway.py`
5. 重建索引：`python scripts/build_index.py`
6. 重启 MToolHub：`docker compose restart mtoolhub`

### 添加新技能

1. 在 `skills/{name}/` 创建目录和 `SKILL.md`
2. 重新导入：`python scripts/import_skills.py`
3. 重建索引：`python scripts/build_index.py`
4. 重启 MToolHub：`docker compose restart mtoolhub`

---

## 性能指标

- **FAISS 检索延迟**: < 50ms（1197 条记录）
- **工具调用端到端**: < 2s（不含 Claude API）
- **对话接口端到端**: < 5s（含 Claude API）
- **内存占用**: ~500MB（MToolHub 容器）
- **GPU 显存**: ~400MB（MAVL 模型）

---

## 文档

- [Phase 1: 基础框架 + 注册表](MToolHub/backend/README_PHASE1.md)
- [Phase 2: 向量检索引擎](MToolHub/backend/README_PHASE2.md)
- [Phase 3: 执行层 + 对话接口](MToolHub/backend/README_PHASE3.md)
- [Phase 4: 数据导入 + Docker 部署](MToolHub/backend/README_PHASE4.md)
- [Gateway 合约规范](gateway/GATEWAY_CONTRACT.md)
- [Claude Code 开发指南](CLAUDE.md)

---

## 故障排查

### MToolHub 无法启动

```bash
# 查看日志
docker compose logs mtoolhub

# 重新构建
docker compose build mtoolhub
docker compose up -d mtoolhub
```

### 无法连接到 Gateway

```bash
# 检查 Gateway 状态
docker compose ps gateway

# 测试网络连接
docker compose exec mtoolhub ping gateway

# 重启 Gateway
docker compose restart gateway
```

### FAISS 索引未找到

```bash
cd MToolHub/backend
python scripts/build_index.py
docker compose restart mtoolhub
```

更多故障排查信息请参考 [README_PHASE4.md](MToolHub/backend/README_PHASE4.md)。

---

## 后续优化方向

1. **会话管理**: Redis 持久化对话历史
2. **结果缓存**: 工具调用结果缓存
3. **监控告警**: Prometheus + Grafana
4. **前端界面**: React 对话式 UI
5. **权限管理**: JWT + RBAC
6. **多语言支持**: 中英文自动切换

---

## 许可证

MIT License

---

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。

---

**⚠️ 医疗免责声明**

本平台提供的所有计算结果和建议仅供医疗专业人员参考，不构成医疗建议。临床决策应基于完整的患者评估和专业判断。
