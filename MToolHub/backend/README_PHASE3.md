# Phase 3: 执行层 + 对话接口

## 概述

Phase 3 完成了 MToolHub 的核心执行逻辑，包括 Claude API 集成、三种资源执行器、编排器以及完整的对话和直接执行接口。

---

## 新增文件

### 1. `app/core/claude_client.py`
**功能：** Claude API 客户端封装

**核心方法：**

#### `extract_parameters()`
从自然语言中提取结构化参数。

**工作原理：**
1. 将工具的参数定义转换为 Claude tool_use 格式
2. 调用 Claude API，让其从用户消息中提取参数
3. 返回结构化的参数字典

**示例：**
```python
# 用户消息："帮我计算 Wells DVT 评分，患者有活动性癌症"
# 工具参数：{"active_cancer": int, "paralysis": int, ...}

result = await claude_client.extract_parameters(
    user_message="帮我计算 Wells DVT 评分，患者有活动性癌症",
    tool_schema={
        "name": "wells_score_dvt",
        "parameters": [
            {"name": "active_cancer", "type": "integer", "description": "活动性癌症"},
            {"name": "paralysis", "type": "integer", "description": "瘫痪"}
        ]
    }
)
# 返回: {"active_cancer": 1, "paralysis": 0, ...}
```

#### `interpret_result()`
将工具输出转换为自然语言解释。

**示例：**
```python
result = await claude_client.interpret_result(
    user_message="帮我计算 Wells DVT 评分",
    tool_result={"score": 3, "risk_level": "moderate"},
    tool_name="Wells Score for DVT"
)
# 返回: "根据计算，Wells DVT 评分为 3 分，属于中度风险..."
```

#### `chat()`
纯对话模式，不调用工具。

**使用场景：**
- 向量检索置信度 < 0.60
- 用户询问一般医学知识
- 无需调用具体工具的咨询

#### `select_and_execute()`
Claude 选择模式，从候选工具中选择最合适的。

**工作原理：**
1. 将 top-3 候选资源转换为 Claude tools
2. Claude 根据用户消息选择并调用工具
3. 返回执行结果

**使用场景：**
- 向量检索置信度在 0.60-0.85 之间
- 多个候选工具相似度接近
- 需要 Claude 进行二次判断

---

### 2. `app/services/executor.py`
**功能：** 执行器抽象基类

**设计模式：** 策略模式（Strategy Pattern）

**接口定义：**
```python
class Executor(ABC):
    @abstractmethod
    async def execute(
        self, 
        resource: dict, 
        user_message: str, 
        arguments: Optional[Dict[str, Any]] = None,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None
    ) -> dict:
        """
        执行资源调用
        
        返回格式：
        {
            "success": bool,
            "result": Any,
            "trace": str,
            "disclaimer": str
        }
        """
        pass
```

---

### 3. `app/services/tool_executor.py`
**功能：** 工具执行器（MDCalc / 单位换算 / 评分工具）

**执行流程：**
```
1. 参数提取
   ├─ 如果 arguments 已提供 → 直接使用
   └─ 否则 → 调用 Claude extract_parameters()

2. 调用 Gateway
   POST http://gateway:9000/tools/{gateway_tool_name}/call
   Body: {"function_name": "...", "arguments": {...}}

3. 结果解释
   调用 Claude interpret_result() 生成自然语言解释

4. 返回结果
   {
     "success": true,
     "result": {
       "raw": {...},           # 原始工具输出
       "interpretation": "..." # Claude 解释
     },
     "trace": "...",
     "disclaimer": "..."
   }
```

**错误处理：**
- Gateway 连接失败：重试 3 次
- 参数提取失败：返回详细错误信息
- 工具调用失败：记录完整追踪信息

---

### 4. `app/services/model_executor.py`
**功能：** 模型执行器（MAVL 胸片分析）

**执行流程：**
```
1. 验证输入
   检查 file_bytes 是否存在

2. 调用 Gateway
   POST http://gateway:9000/tools/{gateway_tool_name}/predict
   Content-Type: multipart/form-data
   Body: 
     - file: 图像文件
     - top_k: 返回前 K 个结果

3. 结果解释
   调用 Claude 解释疾病概率

4. 返回结果
   {
     "success": true,
     "result": {
       "predictions": [...],   # 疾病概率列表
       "interpretation": "..." # Claude 解释
     }
   }
```

**MAVL 输出格式：**
```json
{
  "predictions": [
    {"disease": "effusion", "probability": 0.85},
    {"disease": "pneumonia", "probability": 0.12},
    {"disease": "cardiomegaly", "probability": 0.08}
  ]
}
```

---

### 5. `app/services/skill_executor.py`
**功能：** 技能执行器（Skills）

**技能类型处理：**

#### `document_only`
- 仅加载 `SKILL.md`
- 注入到 Claude system prompt
- 直接调用 Claude chat

#### `tool_reference`
- 加载 `SKILL.md`
- 加载 `references/` 目录下的参考文档（最多 8000 字符）
- 合并后注入 Claude system prompt

#### `executable`
- 加载 `SKILL.md`
- 加载 `coworker.py` 中的 `TOOLS` 列表
- 将 Python 函数转换为 Claude tool_use 格式
- 调用 Claude 并支持工具调用

**coworker.py 格式示例：**
```python
# coworker.py
def check_drug_interaction(drug1: str, drug2: str) -> dict:
    """检查药物相互作用"""
    # 实现逻辑
    return {"interaction": "moderate", "description": "..."}

TOOLS = [check_drug_interaction]
```

#### `complex_workflow`
- Phase 3 暂不支持
- 返回提示信息："此技能类型需要复杂工作流支持，暂未实现"

**执行流程：**
```
1. 加载技能内容
   ├─ SKILL.md（必需）
   ├─ references/（可选）
   └─ coworker.py（可选）

2. 构建 system prompt
   system_prompt = SKILL.md + references + 医疗免责声明

3. 调用 Claude
   ├─ document_only / tool_reference → chat()
   └─ executable → select_and_execute() with tools

4. 返回结果
```

---

### 6. `app/services/orchestrator.py`
**功能：** 编排器，根据路由计划协调执行

**核心方法：**

#### `run()`
主入口，根据 `RoutingPlan.mode` 分发到不同执行模式。

**执行模式：**

##### `chat_only` 模式
```python
# 置信度 < 0.60，纯对话
result = await claude_client.chat(
    user_message=user_message,
    conversation_history=conversation_history
)
```

##### `direct_call` 模式
```python
# 置信度 ≥ 0.85，直接调用
resource = routing_plan.selected_resources[0]
executor = self._get_executor(resource["category"])
result = await executor.execute(
    resource=resource["item"],
    user_message=user_message,
    arguments=arguments,
    file_bytes=file_bytes
)
```

##### `claude_select` 模式
```python
# 置信度 0.60-0.85，Claude 选择
candidates = routing_plan.selected_resources[:3]
result = await claude_client.select_and_execute(
    user_message=user_message,
    candidates=candidates,
    file_bytes=file_bytes
)
```

**执行器选择：**
```python
def _get_executor(self, category: str) -> Executor:
    if category == "tool":
        return tool_executor
    elif category == "model":
        return model_executor
    elif category == "skill":
        return skill_executor
```

---

### 7. `app/routers/chat.py`
**功能：** 对话接口路由

**接口定义：**
```python
POST /api/chat
Content-Type: multipart/form-data

参数：
- message: str (必需) - 用户消息
- file: UploadFile (可选) - 上传的文件（如胸片图像）
- conversation_id: str (可选) - 会话 ID

响应：
{
  "response": str,              # 回复内容
  "tools_used": List[str],      # 使用的工具列表
  "routing_info": {
    "mode": str,                # 路由模式
    "confidence": float,        # 置信度
    "candidates": List[str],    # 候选资源
    "trace": str                # 执行追踪
  },
  "disclaimer": str             # 医疗免责声明
}
```

**执行流程：**
```
1. 接收请求
   ├─ 读取 message
   ├─ 读取 file（如有）
   └─ 读取 conversation_id（如有）

2. 路由决策
   routing_plan = route_decision_maker.decide(
       user_message=message,
       has_file=file is not None,
       file_type=file.content_type
   )

3. 执行
   result = await orchestrator.run(
       user_message=message,
       routing_plan=routing_plan,
       file_bytes=file_bytes,
       filename=filename
   )

4. 返回响应
```

**使用示例：**
```bash
# 纯文本对话
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "帮我计算 Wells DVT 评分，患者有活动性癌症"}'

# 文本 + 图像
curl -X POST http://localhost:8080/api/chat \
  -F "message=分析这张胸片" \
  -F "file=@chest_xray.jpg"
```

---

### 8. `app/routers/execute.py`
**功能：** 直接执行接口路由

**接口定义：**
```python
POST /api/execute
Content-Type: application/json

请求体：
{
  "resource_id": str,           # 资源 ID（如 "tool-mdcalc:wells_score_dvt"）
  "arguments": dict,            # 执行参数
  "context": str (可选)         # 上下文信息
}

响应：
{
  "success": bool,
  "result": Any,
  "trace": str,
  "disclaimer": str
}
```

**执行流程：**
```
1. 查找资源
   resource_info = registry_manager.get_resource_by_id(resource_id)

2. 选择执行器
   executor = {
       "tool": tool_executor,
       "model": model_executor,
       "skill": skill_executor
   }[resource_info["category"]]

3. 执行
   result = await executor.execute(
       resource=resource_info["item"],
       user_message=context,
       arguments=arguments
   )

4. 返回结果
```

**使用示例：**
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
  }'
```

---

## 关键设计决策

### 1. Claude 的双重角色

**参数提取：**
- 问题：用户用自然语言描述，工具需要结构化参数
- 解决：使用 Claude tool_use 功能自动提取参数
- 优势：支持复杂参数、自动类型转换、处理缺失值

**结果解释：**
- 问题：工具输出是 JSON，用户需要自然语言解释
- 解决：将工具输出传给 Claude 生成解释
- 优势：上下文相关、专业术语解释、风险提示

### 2. 执行器模式

**为什么使用策略模式？**
- 三种资源类型（tool / model / skill）调用方式不同
- 需要统一的接口供编排器调用
- 便于后续扩展新的资源类型

**好处：**
- 代码解耦：每个执行器独立实现
- 易于测试：可以单独测试每个执行器
- 易于扩展：新增资源类型只需实现 Executor 接口

### 3. 编排器设计

**为什么需要编排器？**
- 路由决策和执行逻辑分离
- 统一处理三种路由模式
- 集中管理执行流程和错误处理

**职责：**
- 根据路由计划选择执行模式
- 选择合适的执行器
- 处理执行结果和错误
- 生成统一的响应格式

### 4. 技能类型处理

**为什么区分四种类型？**
- `document_only`：最简单，仅需 prompt
- `tool_reference`：需要加载外部文档
- `executable`：需要调用 Python 函数
- `complex_workflow`：需要复杂的多步骤编排

**实现策略：**
- Phase 3 实现前三种（覆盖 95% 的技能）
- `complex_workflow` 留待后续优化

---

## 错误处理

### 1. Gateway 连接失败
```python
try:
    resp = await client.post(gateway_url, json=data, timeout=60.0)
except httpx.TimeoutException:
    return {"success": False, "error": "Gateway 响应超时"}
except httpx.ConnectError:
    return {"success": False, "error": "无法连接到 Gateway"}
```

### 2. Claude API 失败
```python
try:
    message = await claude_client.extract_parameters(...)
except anthropic.APIError as e:
    return {"success": False, "error": f"Claude API 错误: {e}"}
```

### 3. 参数验证失败
```python
# Pydantic 自动验证
try:
    request = ExecuteRequest(**request_data)
except ValidationError as e:
    raise HTTPException(status_code=422, detail=str(e))
```

---

## 测试验证

### 单元测试（待补充）
```bash
pytest tests/test_executor.py -v
pytest tests/test_orchestrator.py -v
pytest tests/test_claude_client.py -v
```

### 集成测试
```bash
# 测试工具调用
curl -X POST http://localhost:8080/api/chat \
  -d '{"message": "计算 SOFA 评分"}'

# 测试模型调用
curl -X POST http://localhost:8080/api/chat \
  -F "message=分析胸片" \
  -F "file=@test.jpg"

# 测试技能调用
curl -X POST http://localhost:8080/api/chat \
  -d '{"message": "如何写临床报告？"}'
```

---

## 性能优化

### 1. 异步执行
所有 I/O 操作使用 `async/await`：
- Claude API 调用
- Gateway HTTP 请求
- 文件读取

### 2. 连接池
使用 `httpx.AsyncClient` 复用连接：
```python
async with httpx.AsyncClient(timeout=60.0) as client:
    # 复用连接
```

### 3. 超时控制
所有外部调用设置超时：
- Gateway 调用：60 秒
- Claude API：30 秒

---

## 医疗免责声明

所有响应都包含免责声明：
```
⚠️ 医疗免责声明：
本平台提供的计算结果和建议仅供医疗专业人员参考，不构成医疗建议。
临床决策应基于完整的患者评估和专业判断。
```

---

## Phase 3 完成清单

- [x] `app/core/claude_client.py` - Claude API 客户端
- [x] `app/services/executor.py` - 执行器基类
- [x] `app/services/tool_executor.py` - 工具执行器
- [x] `app/services/model_executor.py` - 模型执行器
- [x] `app/services/skill_executor.py` - 技能执行器
- [x] `app/services/orchestrator.py` - 编排器
- [x] `app/routers/chat.py` - 对话接口
- [x] `app/routers/execute.py` - 直接执行接口
- [x] 更新 `app/routers/__init__.py`
- [x] 更新 `app/services/__init__.py`
- [x] 更新 `app/main.py`

**状态：** ✅ Phase 3 完成
