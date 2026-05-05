# Gateway API 文档

统一推理网关的接口说明。所有工具通过网关统一对外，调用方只需对接本文档。

## 基础信息

| 项目 | 值 |
|---|---|
| 服务地址 | `http://<服务器IP>:9000` |
| 交互式文档 | `http://<服务器IP>:9000/docs`（Swagger，可直接在网页测试） |
| 接口规范 | `http://<服务器IP>:9000/openapi.json` |

---

## 接口列表

### GET /health
网关健康状态及 GPU 使用情况。

```bash
curl http://localhost:9000/health
```

```json
{
    "status": "ok",
    "total_gpu_mb": 40000,
    "used_mb": 400,
    "free_mb": 39600,
    "loaded_models": {
        "mavl": {"gpu_mb": 400, "idle_s": 12.3}
    }
}
```

---

### GET /tools
列出所有已注册工具及其加载状态。

```bash
curl http://localhost:9000/tools
```

```json
{
    "mavl": {
        "description": "...",
        "type": "remote",
        "input": "image",
        "output": "disease_probabilities",
        "gpu_memory_mb": 400,
        "loaded": true
    }
}
```

---

### GET /tools/{tool_name}/info
查询单个工具的完整配置信息。

```bash
curl http://localhost:9000/tools/mavl/info
```

---

### POST /tools/{tool_name}/predict
核心推理接口。上传文件，转发给对应工具，返回推理结果。

**请求格式：** `multipart/form-data`

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `file` | file | 是 | 输入文件，具体格式由各工具决定 |
| `top_k` | int | 否，默认 5 | 返回概率最高的 K 个结果 |

```bash
curl -X POST http://localhost:9000/tools/mavl/predict \
  -F "file=@/path/to/input.jpg" \
  -F "top_k=5"
```

```python
import requests
resp = requests.post(
    "http://localhost:9000/tools/mavl/predict",
    files={"file": ("xray.jpg", open("xray.jpg", "rb"), "image/jpeg")},
    data={"top_k": 5},
)
print(resp.json())
```

**HTTP 错误码：**

| 状态码 | 含义 |
|---|---|
| 404 | 工具名不存在 |
| 413 | 文件过大 |
| 415 | 文件格式不支持 |
| 503 | 模型加载失败（GPU 不足等） |
| 504 | 推理超时 |

**注意：** 首次调用某工具时，网关自动触发模型加载（约 20–30 秒），请求会阻塞等待完成，**无需重试**。

---

## 新增工具说明

在 `gateway/tools/` 下新建文件夹并放入 `config.yaml`，重启网关后自动注册，无需修改任何代码。

```yaml
# gateway/tools/<tool_name>/config.yaml 最小示例
name: my-tool
type: remote
endpoint: http://my-tool:8000
gpu_memory_mb: 2000
description: "工具描述"
input: image
output: classification
```
