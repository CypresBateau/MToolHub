# Gateway 接入规范

> 向 Claude Code 提供的参考文档。每次新增工具服务时，必须对照本文档检查所有约定，避免因上下文丢失导致接口不兼容。

---

## 一、Gateway 对每个服务的调用规范

Gateway 会主动调用各服务的以下端点，**路径和方法不可更改**：

| 调用时机 | Gateway 发送的请求 | 代码位置 |
|----------|-------------------|----------|
| 工具首次被调用时 | `POST {endpoint}/load` | `scheduler.py:_call_load()` |
| LRU 驱逐时 | `POST {endpoint}/unload` | `scheduler.py:_call_unload()` |
| 转发计算请求 | `POST {endpoint}/api/v1/call` | `main.py:call_tool()` |
| 转发图像推理 | `POST {endpoint}/api/v1/predict` | `main.py:predict()` |
| （健康检查由 Docker 自身完成，Gateway 不调用） | — | — |

**关键规则：**
- `/load` 和 `/unload` 必须挂载在**根路径**，不能加 `/api/v1` 前缀
- `/call` 和 `/predict` 必须挂载在 `/api/v1/` 前缀下
- 三者不能混淆，这是本规范存在的根本原因（曾因此引发 404 错误）

---

## 二、服务端必须实现的端点

### 必须实现（所有服务）

```
POST /load              → 返回 {"status": "ok"}，HTTP 200
POST /unload            → 返回 {"status": "unloaded"}，HTTP 200
GET  /health            → 返回健康状态 JSON，HTTP 200
POST /api/v1/call       → 执行工具，返回结果（JSON 工具类服务）
POST /api/v1/predict    → 执行推理，返回结果（图像类服务）
```

### GPU 服务（如 MAVL）
`/load` 需要真正加载模型权重到 GPU，耗时较长（20–30 秒）。

### CPU 服务（如 tool-mdcalc、tool-unit）
`/load` 和 `/unload` 是 **no-op**，只翻转一个 `loaded` 布尔标志，立即返回。工具在服务启动时已全部加载到内存。

---

## 三、gateway/tools/{name}/config.yaml 字段说明

```yaml
name: tool-mdcalc          # 工具名，必须与文件夹名一致，Gateway 用此名路由请求
type: remote               # 固定填 remote
endpoint: http://tool-mdcalc:8000   # Docker 内网地址，hostname 必须与 container_name 一致
gpu_memory_mb: 0           # GPU 显存占用（MB）。CPU 工具填 0，GPU 工具填实际大小
load_time_s: 10            # /load 请求的超时时间（秒），CPU 工具填 5–10，GPU 工具填 60+
call_timeout_s: 15         # /api/v1/call 请求的超时时间（秒）
description: "..."         # 工具描述，通过 GET /tools 暴露给外部
input: json                # 输入类型：json（计算器）或 image（图像推理）
output: dict               # 输出类型：描述性字符串，不影响逻辑
```

**`gpu_memory_mb: 0` 的含义：**
Scheduler 跳过显存检查，直接调用 `/load`（no-op），然后立即转发请求。CPU 工具不参与 LRU 驱逐。

---

## 四、docker-compose.yml 服务配置规范

```yaml
tool-mdcalc:
  build: ./mdcalc            # 构建目录，对应 toolkit/mdcalc/
  image: mdcalc:latest       # 镜像名，build 一次后两个服务可共用同一镜像
  container_name: tool-mdcalc  # 必须与 config.yaml 中 endpoint 的 hostname 一致
  expose:
    - "8000"                 # 只暴露给 Docker 内网，不用 ports（外部不可直接访问）
  environment:
    - TOOL_JSON_PATH=/data/tools_metadata.json
  volumes:
    - /data/wxb/toolkit/tools_metadata.json:/data/tools_metadata.json:ro
  networks:
    - toolnet                # 必须与 gateway 在同一网络
  restart: unless-stopped
```

**`expose` vs `ports` 区别：**
- `expose: ["8000"]`：仅 Docker 内网可达，外部无法直接访问（正确做法）
- `ports: ["8001:8000"]`：宿主机可直接访问，仅调试时使用

---

## 五、新增服务完整检查清单

新建一个 B 类工具服务时，逐项核对：

- [ ] `lifecycle.py` 的 router **不加** `/api/v1` 前缀（`router = APIRouter()`）
- [ ] `/load` 和 `/unload` 路径为根路径
- [ ] `/call` 或 `/predict` 路径在 `APIRouter(prefix="/api/v1")` 下
- [ ] `container_name` 与 `config.yaml` 中 `endpoint` 的 hostname 完全一致
- [ ] 服务加入 `toolnet` 网络
- [ ] 使用 `expose` 而非 `ports`
- [ ] `gateway` 的 `depends_on` 已加入新服务名
- [ ] 数据文件已上传到远程宿主机对应路径

---

## 六、部署操作顺序

```bash
# 1. 构建新服务镜像
docker compose build <service-name>

# 2. 启动新服务
docker compose up -d <service-name>

# 3. 确认服务启动正常
docker logs <service-name>

# 4. gateway 仅需 restart（config.yaml 变更无需 rebuild）
docker compose restart gateway

# 5. 若修改了 gateway/app/ 代码（如 main.py），则需要 rebuild
docker compose build gateway && docker compose up -d gateway
```

> **重要：** 修改 `gateway/app/` 代码后必须 `build gateway`，仅 `restart` 不会生效。
> 修改 `gateway/tools/*/config.yaml` 后只需 `restart gateway`。
