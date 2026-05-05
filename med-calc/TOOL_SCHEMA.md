# 医疗工具 JSON 字段规范

> 用于指导 LLM 从网页抓取工具信息并整理为标准 JSON 格式。

---

## 一、字段规范

### 1.1 通用必填字段（scale / unit 均需）

| 字段 | 类型 | 说明 |
|------|------|------|
| `function_name` | `str` | Python 合法函数名，小写+下划线，如 `calculate_sofa_score` |
| `tool_name` | `str` | 工具的完整可读名称，如 `"SOFA Score"` |
| `category` | `str` | 工具类别：`"scale"`（评分）或 `"unit"`（单位换算） |
| `description` | `str` | 工具用途的完整描述，用于向量检索，需包含适应症、使用场景 |
| `docstring` | `str` | 函数文档字符串，**必须包含 Parameters 和 Returns 两节**（见格式要求） |
| `parameters` | `list` | 结构化参数列表（从 docstring 解析/生成，见下） |
| `returns` | `object` | 结构化返回值描述（见下） |
| `code` | `str` | 完整可执行的 Python 函数源码字符串 |

### 1.2 scale 专属字段

| 字段 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `formula` | `str` | 必填 | 评分计算规则，列出各变量和对应分值 |
| `next_steps` | `str` | 选填 | 评分结果对应的临床建议或解释 |

### 1.3 unit 专属字段

| 字段 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `units_list` | `list[str]` | 必填 | 该工具支持的所有单位，如 `["mmol/L", "mg/dL"]`，顺序即为 `input_unit`/`target_unit` 的索引 |

---

## 二、子结构格式

### parameters 列表（每个参数一个对象）

```json
{
  "name": "age",
  "type": "int",
  "description": "Patient age in years"
}
```

- `type` 取值：`int` / `float` / `bool` / `str` / `list of int` / `list of float`
- `description` 需注明单位、取值范围或枚举含义，如 `"0=No, 1=Yes"`

### returns 对象

```json
{
  "type": "int",
  "description": "The calculated SOFA score (0–24)"
}
```

### docstring 格式要求

```
{工具一句话说明}

Parameters:
{param_name} ({type}): {描述，含单位/枚举}
...

Returns:
{type}: {返回值说明}
```

---

## 三、完整示例

### scale 工具

```json
{
  "function_name": "calculate_sofa_score",
  "tool_name": "SOFA Score (Sequential Organ Failure Assessment)",
  "category": "scale",
  "description": "The SOFA score assesses organ dysfunction in ICU patients across six systems: respiration, coagulation, liver, cardiovascular, CNS, and renal. Used to predict ICU mortality.",
  "formula": "Sum of subscores:\n- Respiration (PaO2/FiO2): 0–4 pts\n- Coagulation (platelets): 0–4 pts\n- Liver (bilirubin): 0–4 pts\n- Cardiovascular (MAP/vasopressors): 0–4 pts\n- CNS (GCS): 0–4 pts\n- Renal (creatinine/urine): 0–4 pts",
  "next_steps": "Score ≥2: suspected sepsis-related organ dysfunction. Score >11: mortality >90%.",
  "docstring": "Calculate the SOFA score for ICU patients.\n\nParameters:\nrespiration (int): PaO2/FiO2 score 0-4\ncoagulation (int): Platelet score 0-4\nliver (int): Bilirubin score 0-4\ncardiovascular (int): MAP/vasopressor score 0-4\ncns (int): GCS score 0-4\nrenal (int): Creatinine/urine output score 0-4\n\nReturns:\nint: Total SOFA score (0-24)",
  "parameters": [
    {"name": "respiration",   "type": "int", "description": "PaO2/FiO2 score 0-4"},
    {"name": "coagulation",   "type": "int", "description": "Platelet score 0-4"},
    {"name": "liver",         "type": "int", "description": "Bilirubin score 0-4"},
    {"name": "cardiovascular","type": "int", "description": "MAP/vasopressor score 0-4"},
    {"name": "cns",           "type": "int", "description": "GCS score 0-4"},
    {"name": "renal",         "type": "int", "description": "Creatinine/urine output score 0-4"}
  ],
  "returns": {"type": "int", "description": "Total SOFA score (0-24)"},
  "code": "def calculate_sofa_score(respiration, coagulation, liver, cardiovascular, cns, renal):\n    return respiration + coagulation + liver + cardiovascular + cns + renal"
}
```

### unit 工具

```json
{
  "function_name": "convert_glucose_unit",
  "tool_name": "Glucose, 血糖",
  "category": "unit",
  "description": "Convert Glucose measurements between units.\nunits list = ['mmol/L', 'mg/dL']",
  "units_list": ["mmol/L", "mg/dL"],
  "docstring": "Convert the value of Glucose from input_unit to target_unit.\n\nParameters:\ninput_value (float): Input value to convert\ninput_unit (int): Index in units_list (0-based)\ntarget_unit (int): Index in units_list (0-based)\n\nReturns:\nstr: Conversion result, e.g. '5.0 mmol/L = 90.09 mg/dL'",
  "parameters": [
    {"name": "input_value", "type": "float", "description": "Input numeric value"},
    {"name": "input_unit",  "type": "int",   "description": "Source unit index (0-based), maps to units_list"},
    {"name": "target_unit", "type": "int",   "description": "Target unit index (0-based), maps to units_list"}
  ],
  "returns": {"type": "str", "description": "Natural language result, e.g. '5.0 mmol/L = 90.09 mg/dL'"},
  "code": "def convert_glucose_unit(input_value, input_unit, target_unit):\n    factors = [1, 18.018]\n    result = input_value / factors[input_unit] * factors[target_unit]\n    units = ['mmol/L', 'mg/dL']\n    return f'{input_value} {units[input_unit]} = {round(result, 4)} {units[target_unit]}'"
}
```

---

## 四、给 LLM 的提取要点

从网页抓取时需要重点获取的信息：

1. **工具名称和类别** — 标题区域，判断是评分类还是换算类
2. **适应症/用途** — 工具描述段落，直接作为 `description`
3. **输入变量** — 计算器的每个输入项，提取：变量名、数据类型、单位、枚举选项
4. **计算公式** — 分值表或公式说明，整理为 `formula`（scale）
5. **可支持的单位** — 所有可互转的单位，整理为 `units_list`（unit）
6. **结果解读** — 不同分值段的临床意义，整理为 `next_steps`（scale，选填）
7. **Python 实现** — 根据公式生成可执行函数，函数名用 `function_name`
