# MToolHub Backend - Phase 1 功能说明

## 概述

Phase 1 实现了 MToolHub 后端的基础框架和注册表管理功能。

## 已实现功能

### 1. 配置管理 (`app/config.py`)
- 使用 pydantic-settings 管理所有配置项
- 支持从环境变量和 .env 文件加载
- 包含 Gateway、Claude API、Embedding 模型、路由阈值等配置

### 2. 数据模型 (`app/models/`)
- **registry.py**: 定义三种资源的元数据结构
  - `ToolMetadata`: 工具元数据
  - `ModelMetadata`: 模型元数据
  - `SkillMetadata`: 技能元数据
- **api.py**: 定义 API 请求和响应数据结构
  - `ChatRequest/ChatResponse`: 对话接口
  - `ExecuteRequest/ExecuteResponse`: 直接执行接口
  - `RoutingPlan`: 路由计划
  - `ToolSearchRequest/ToolSearchResponse`: 工具搜索接口

### 3. 注册表管理 (`app/core/registry.py`)
- `RegistryManager`: 注册表管理器
  - 从 JSON 文件加载三类资源
  - 提供按 ID 查询资源的方法
  - 支持获取所有资源列表
  - 支持重新加载注册表

### 4. FastAPI 应用 (`app/main.py`)
- FastAPI 应用入口
- 配置 CORS 中间件
- 注册路由模块
- 启动和关闭事件处理

### 5. 路由模块 (`app/routers/`)
- **health.py**: 健康检查接口
  - `GET /health`: 返回服务状态和资源统计
- **tools.py**: 工具管理接口
  - `GET /api/tools`: 获取工具列表（支持分页和过滤）
  - `GET /api/tools/{resource_id}`: 获取工具详情

### 6. 工具模块 (`app/utils/`)
- **disclaimer.py**: 医疗免责声明工具
  - `get_disclaimer()`: 获取免责声明
  - `add_disclaimer_to_response()`: 在响应中添加免责声明

### 7. 示例数据 (`data/registry/`)
- **tools.json**: 3 个示例工具
  - Wells Score for DVT
  - CHA2DS2-VASc Score
  - Glucose Unit Conversion
- **models.json**: 1 个示例模型
  - MAVL Chest X-Ray Analysis
- **skills.json**: 2 个示例技能
  - Clinical Report Generation
  - Care Coordination

## 目录结构

```
MToolHub/backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 入口
│   ├── config.py               # 配置管理
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── registry.py         # 注册表模型
│   │   └── api.py              # API 模型
│   ├── routers/                # 路由模块
│   │   ├── __init__.py
│   │   ├── health.py           # 健康检查
│   │   └── tools.py            # 工具管理
│   ├── core/                   # 核心模块
│   │   ├── __init__.py
│   │   └── registry.py         # 注册表管理
│   ├── services/               # 服务模块（待实现）
│   │   └── __init__.py
│   └── utils/                  # 工具模块
│       ├── __init__.py
│       └── disclaimer.py       # 免责声明
├── data/
│   ├── registry/               # 注册表 JSON
│   │   ├── tools.json
│   │   ├── models.json
│   │   └── skills.json
│   └── indexes/                # FAISS 索引（待生成）
├── scripts/                    # 脚本（待实现）
├── tests/                      # 测试（待实现）
├── requirements.txt            # Python 依赖
└── .env.example                # 环境变量示例
```

## 如何运行

### 1. 安装依赖
```bash
cd MToolHub/backend
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入 CLAUDE_API_KEY
```

### 3. 启动服务
```bash
python -m app.main
# 或
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### 4. 访问 API 文档
打开浏览器访问：http://localhost:8080/docs

## API 接口

### 健康检查
```bash
curl http://localhost:8080/health
```

### 获取工具列表
```bash
# 获取所有资源
curl http://localhost:8080/api/tools

# 按类别过滤
curl "http://localhost:8080/api/tools?category=tool"

# 分页
curl "http://localhost:8080/api/tools?limit=10&offset=0"
```

### 获取工具详情
```bash
curl http://localhost:8080/api/tools/tool_mdcalc_wells_dvt
```

## 下一步

Phase 2 将实现：
- Embedding 模型加载
- FAISS 索引构建和检索
- 路由决策逻辑
- 工具搜索接口
