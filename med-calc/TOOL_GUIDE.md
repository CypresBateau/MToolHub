# Med-Calc Tool Guide

医疗评分计算器和单位换算工具的 API 使用说明。

---

## 工具概览

| 服务名 | 工具数 | 说明 |
|--------|--------|------|
| `tool-scale` | 44 | 临床评分计算器（SOFA、APACHE II、ARISCAT 等） |
| `tool-unit` | 237 | 医学单位换算（mmol/L ↔ mg/dL 等） |

两个服务共用同一个 Docker 镜像（`med-calc:latest`），通过环境变量区分工具集。

---

## 通过 Gateway 调用（推荐）

Gateway 地址：`http://<host>:9000`

### 查询可用工具

```bash
# 查看所有已注册工具（含 mavl、tool-scale、tool-unit）
curl http://localhost:9000/tools

# 查看某个具体工具的详情（docstring / formula）
curl http://localhost:9000/tools/tool-scale/info
```

### 执行计算器工具

```bash
POST /tools/{tool_name}/call
Content-Type: application/json

{
  "function_name": "<函数名>",
  "arguments": {
    "<参数名>": <值>,
    ...
  }
}
```

**示例：ARISCAT 评分**

```bash
curl -X POST http://localhost:9000/tools/tool-scale/call \
  -H "Content-Type: application/json" \
  -d '{
    "function_name": "calculate_ariscat_score",
    "arguments": {
      "age": 65,
      "spo2": 94,
      "respiratory_infection": 0,
      "anemia": 1,
      "surgical_incision": 1,
      "surgery_duration": 2.5,
      "emergency": 0
    }
  }'
```

响应：

```json
{
  "function_name": "calculate_ariscat_score",
  "tool_name": "ARISCAT Score for Postoperative Pulmonary Complications",
  "category": "scale",
  "result": 26
}
```

**示例：单位换算（钾离子）**

```bash
curl -X POST http://localhost:9000/tools/tool-unit/call \
  -H "Content-Type: application/json" \
  -d '{
    "function_name": "convert_potassium_k_unit",
    "arguments": {
      "input_value": 4.5,
      "input_unit": 0,
      "target_unit": 1
    }
  }'
```

响应：

```json
{
  "function_name": "convert_potassium_k_unit",
  "tool_name": "Potassium (K), 钾 (K)",
  "category": "unit",
  "result": "4.5 mmol/L = 4.5 mEq/L"
}
```

> `input_unit` / `target_unit` 是单位列表的索引（0-based），具体单位列表见工具的 `description` 字段。

---

## 参数格式兼容性

`arguments` 支持两种格式，服务自动识别：

```json
// 纯值格式（推荐）
{"age": 65, "spo2": 94}

// LLM 输出格式（Value/Unit 包装）
{"age": {"Value": 65, "Unit": "years"}, "spo2": {"Value": 94, "Unit": "%"}}
```

---

## 查询工具列表（直连容器）

```bash
# 直连 tool-scale 容器（需在同一 Docker 网络或开放端口）
curl http://localhost:8001/api/v1/tools        # 列出所有 scale 工具
curl http://localhost:8001/api/v1/tools/calculate_ariscat_score  # 工具详情（含 docstring）
```

---

## 部署说明

### 远程主机路径

需将 JSON 文件放在宿主机上，并在 `docker-compose.yml` 中挂载：

```yaml
tool-scale:
  volumes:
    - /data/wxb/toolkit/tool_scale.json:/data/tool_scale.json:ro

tool-unit:
  volumes:
    - /data/wxb/toolkit/tool_unit.json:/data/tool_unit.json:ro
```

### 构建和启动

```bash
cd /data/wxb/toolkit

# 首次构建
docker compose build tool_scale（tool_unit也可以，他们对应同一个build的镜像叫做med-calc）   # 只需构建一次，两个服务共用

# 启动所有服务
docker compose up -d

# 查看日志
docker logs tool-scale
docker logs tool-unit
docker logs toolkit-gateway
```

### 健康检查

```bash
curl http://localhost:9000/health
curl http://localhost:8001/health   # tool-scale（需开放端口或在容器内）
curl http://localhost:8002/health   # tool-unit
```
