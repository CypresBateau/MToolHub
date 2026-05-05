# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**用户语言：中文。所有回复、注释、文档请默认使用中文。**

---

## 项目概述

**MToolHub** — 医疗工具智能调度平台，构建在已有 Gateway 服务之上。目标是新增一个语义路由层（FAISS + 医学 Embedding 模型），接受自然语言查询并路由到三类资源：

1. **医疗计算工具**（CPU）— 871 个 MDCalc 计算器（`tool-mdcalc`）、237 个单位换算工具（`tool-unit`）、44 个评分计算器（`tool-scale`，当前禁用）
2. **医疗 AI 模型**（GPU）— MAVL 胸片分析模型（`mavl`），后续会持续新增
3. **医疗技能 Skills**（LLM）— `skills/` 目录下约 88 个技能，每个是含 `SKILL.md` + 可选 `references/` 和/或 `coworker.py` 的文件夹

MToolHub 后端是**独立的 FastAPI 服务**，位于已有 Gateway 前面，不替换 Gateway。

---

## 已有基础设施

### Gateway（`gateway/`）
- 运行在端口 **9000**，将请求转发到 Docker 内网（`toolnet`）的工具容器
- 两种转发接口：
  - `POST /tools/{tool_name}/predict` — multipart/form-data，用于图像推理（MAVL）
  - `POST /tools/{tool_name}/call` — JSON `{function_name, arguments}`，用于计算器
- 工具注册：在 `gateway/tools/{name}/` 下放 `config.yaml`，然后 `docker compose restart gateway`
- GPU 调度：`scheduler.py` 通过 `POST {endpoint}/load` 和 `POST {endpoint}/unload` 实现 LRU 驱逐

**关键路径规则（见 `gateway/GATEWAY_CONTRACT.md`）：**
- `/load` 和 `/unload` 必须在根路径（不加 `/api/v1` 前缀）
- `/call` 和 `/predict` 必须在 `/api/v1/` 前缀下
- docker-compose 中的 `container_name` 必须与 `config.yaml` 里 `endpoint` 的 hostname 完全一致
- 工具容器用 `expose` 不用 `ports`（只允许 Gateway 访问）

### MDCalc 服务（`mdcalc/`）
- 从 `tools_metadata.json` 加载 871 个工具（路径通过 `TOOL_JSON_PATH` 环境变量设置）
- 工具通过 `exec()` 执行元数据 JSON 中的 `generated_code` 字段
- `arguments` 支持纯值格式 `{"age": 65}` 和 LLM 包装格式 `{"age": {"Value": 65, "Unit": "years"}}`，executor 自动展开
- 使用 **pydantic v1**（`<2.0`）

### Med-calc 服务（`med-calc/`）
- `tool-scale` 和 `tool-unit` 共用同一个 Docker 镜像 `med-calc:latest`
- 通过 `TOOL_JSON_PATH` 环境变量区分工具集，分别指向 `tool_scale.json` 或 `tool_unit.json`
- 工具 JSON 文件在远程宿主机 `/data/wxb/toolkit/`

### MAVL 模型（`MAVL/`）
- Checkpoint：`checkpoint_full_46.pth`（~400MB），GPU 显存占用约 400MB，加载时间约 20–30 秒
- 输出 75 种胸部病变类别的概率；临床关注类别：`effusion`、`pneumothorax`、`edema`、`atelectasis`、`consolidation`、`pneumonia`、`cardiomegaly`、`nodule`、`mass`、`fracture`
- 通过 Gateway 的 `/predict` 接口调用

### Skills（`skills/`）
- 88 个技能目录，每个含 `SKILL.md` prompt 模板
- 技能类型由目录内容决定：
  - 仅 `SKILL.md` → `document_only`
  - `SKILL.md` + `references/` → `tool_reference`
  - `SKILL.md` + `coworker.py`（导出 `TOOLS` 列表）→ `executable`
  - `SKILL.md` + 大型数据/repo → `complex_workflow`
- 注意：现有 skills 使用 `coworker.py`（而非规划文档中的 `handler.py`），实现时以实际文件名为准

---

## MToolHub 后端架构（待构建）

规划位置：`MToolHub/backend/`（新目录）。核心设计来自 `1.txt`：

```
用户请求
    ↓
MToolHub Backend（FastAPI，端口 8080）
    ├── API 层       — POST /api/chat, GET /api/tools, GET /api/tools/search
    ├── 路由层       — FAISS 向量检索 → 路由决策（高/中/低置信度）
    └── 执行层       — 分发到 Tool / Model / Skill 执行器
            ↓
    已有 Gateway（端口 9000）
            ↓
    tool-mdcalc / tool-unit / tool-scale / mavl 容器
```

### 路由策略（三种模式）
- **`direct_call`**（score ≥ 0.85）：直接调用匹配资源；用 Claude 从自然语言中提取参数，再解读结果
- **`claude_select`**（0.60–0.85）：将 top-3 候选作为 tools 传给 Claude，由 Claude 选择
- **`chat_only`**（score < 0.60）：纯 Claude 对话，不调用工具

### FAISS 索引
- 三个独立索引：`tool`、`model`、`skill`
- 索引文本 = `"{name}. {description}. {description_zh}. Keywords: {keywords}"`
- Embedding 模型：`pritamdeka/S-PubMedBert-MS-MARCO`（~420MB，HuggingFace 直接下载，无需申请）
- 备选：`NeuML/pubmedbert-base-embeddings`（更轻量）
- 注册表 JSON 变更后需重建索引：`python scripts/build_index.py`

### Skill 执行
将 `SKILL.md` 注入 Claude 的 system prompt。`executable` 类型还需将 `coworker.py` 的 `TOOLS` 列表注册为 Claude `tool_use` 工具。

### 医疗输出免责声明
所有 Claude system prompt 必须包含：**"仅供参考，不构成医疗建议。"**

---

## 关键数据位置

| 资源 | 位置 |
|---|---|
| MDCalc 工具元数据 JSON | `/data/wxb/toolkit/tools_metadata.json`（远程宿主机） |
| tool-scale JSON | `/data/wxb/toolkit/tool_scale.json`（远程宿主机） |
| tool-unit JSON | `/data/wxb/toolkit/tool_unit.json`（远程宿主机） |
| MAVL checkpoint | `/data/MAVL/checkpoints/checkpoint_full_46.pth`（远程宿主机） |
| MDCalc 源函数 | `D:\01_work\toolkit\MedMCP-Calc\med-tool-generator\outputs\`（本地 Windows） |

---

## 常用命令

### Gateway
```bash
# 修改 gateway/app/ 代码后重建
docker compose build gateway && docker compose up -d gateway

# 仅修改 config.yaml 后重启
docker compose restart gateway

# 新增工具服务
docker compose build <service-name>
docker compose up -d <service-name>
docker compose restart gateway
```

### 测试工具调用
```bash
# 调用 MDCalc 计算器
curl -X POST http://localhost:9000/tools/tool-mdcalc/call \
  -H "Content-Type: application/json" \
  -d '{"function_name": "wells_score_dvt", "arguments": {"active_cancer": 0, "paralysis": 0}}'

# 调用 MAVL 胸片分析
curl -X POST http://localhost:9000/tools/mavl/predict \
  -F "file=@chest_xray.jpg" \
  -F "top_k=5" | python3 -m json.tool

# 查看所有已注册工具
curl http://localhost:9000/tools
```

### MToolHub 后端（构建后）
```bash
cd MToolHub/backend
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# 构建 FAISS 索引（注册表 JSON 变更后运行）
python scripts/build_index.py

# 从 MDCalc 元数据导入注册表
python scripts/import_mdcalc_tools.py

# 从 skills/ 目录导入技能注册表
python scripts/import_skills.py

# 运行测试
pytest tests/
pytest tests/test_router.py  # 仅向量检索测试
```

---

## 技术选型

| 组件 | 选择 |
|---|---|
| 后端框架 | FastAPI + uvicorn |
| 已有服务 | pydantic v1（`<2.0`） |
| MToolHub 后端 | pydantic v2 + pydantic-settings |
| 向量数据库 | FAISS（`faiss-cpu`） |
| Embedding | `sentence-transformers` + `pritamdeka/S-PubMedBert-MS-MARCO` |
| LLM | Claude API（`anthropic` SDK），模型 `claude-sonnet-4-20250514` |
| HTTP 客户端 | `httpx`（异步） |
| 前端（后续） | React + TypeScript + TailwindCSS + Zustand |

---

## 新增工具/模型到 Gateway 的步骤

1. 创建 `gateway/tools/{name}/config.yaml`，填写必要字段（`name`、`type`、`endpoint`、`gpu_memory_mb` 等）
2. 在 `docker-compose.yml` 中添加服务，`container_name` 必须与 `endpoint` hostname 一致，使用 `expose` 不用 `ports`，加入 `toolnet` 网络
3. 服务必须实现：`POST /load`、`POST /unload`、`GET /health`、`POST /api/v1/call` 或 `POST /api/v1/predict`
4. `docker compose build <name> && docker compose up -d <name> && docker compose restart gateway`

CPU 工具：`/load` 和 `/unload` 是 no-op（只翻转布尔标志）。GPU 工具：`/load` 需真正加载模型权重（MAVL 级别约 20–30 秒）。
