# med-calc 工具库说明

## 概述

本库包含 **871 个医疗计算器工具函数**，全部由 MDCalc.com 的公式数据自动生成，覆盖急诊、心内科、肾内科、神经科、肿瘤科等主要临床场景。

---

## 文件结构

```
outputs/tools/
├── __init__.py                          # 统一入口，导出全部 871 个函数
├── 19_absolute-neutrophil-count-anc.py
├── 23_apgar-score.py
├── 31_calcium-correction-hypoalbuminemia.py
├── ...                                  # 命名规则：{calc_id}_{slug}.py
└── 10662_ses-cd.py

outputs/tools_metadata.json              # 871 条结构化元数据
outputs/docs/
├── api_reference.md                     # Markdown 格式 API 文档
├── api_reference.json                   # 机器可读 API 规范
└── index.md                             # 工具索引表
```

**绝对路径（本机）：**
```
D:\01_work\toolkit\MedMCP-Calc\med-tool-generator\outputs\tools\
D:\01_work\toolkit\MedMCP-Calc\med-tool-generator\outputs\tools_metadata.json
D:\01_work\toolkit\MedMCP-Calc\med-tool-generator\outputs\docs\api_reference.json
D:\01_work\toolkit\MedMCP-Calc\med-tool-generator\outputs\docs\api_reference.md
D:\01_work\toolkit\MedMCP-Calc\med-tool-generator\outputs\docs\index.md
```

**相对路径（以 `med-tool-generator/` 为根）：**
```
outputs/tools/
outputs/tools_metadata.json
outputs/docs/api_reference.json
outputs/docs/api_reference.md
outputs/docs/index.md
```

---

## 函数规范

每个 `.py` 文件包含一个独立函数，命名为工具名称的 snake_case 形式。

**函数签名示例：**
```python
def wells_score_dvt(
    active_cancer: int,
    paralysis: int,
    bedridden: int,
    ...
    alternative_diagnosis: int
) -> dict:
```

**统一约定：**

| 项目 | 规范 |
|------|------|
| 参数单位 | 全部使用 SI 单位（kg、cm、mmol/L 等），函数内部做换算 |
| 分类参数类型 | `str`，有效值在 docstring 中列出，例如 `"Male" \| "Female"` |
| 连续参数类型 | `float` 或 `int`，带有效范围说明 |
| 可选参数 | 排在必填参数之后，默认值为 `None` |
| 输入验证 | 越界时 `raise ValueError`，消息说明具体条件 |
| 返回值 | 统一返回 `dict` |

**返回值结构（各 key 出现频率）：**

| Key | 出现比例 | 含义 |
|-----|------|------|
| `interpretation` | 99% | 必含数值 + 风险分级 + 临床建议的完整文字说明 |
| `risk_category` | 68% | 风险/严重程度分级字符串 |
| `score` | 61% | 主要数值计算结果 |
| `result` | 7% | 用于非评分类工具（如剂量计算） |
| `classification` | 7% | 用于诊断分类工具 |
| 其他扩展 key | 按需 | 如 `ibw_kg`、`fluid_rate_ml_hr`、`tbw_l` 等临床派生值 |

**`__init__.py`** 通过 `importlib` 动态加载所有模块（因文件名以数字开头），可直接 `from tools import <function_name>` 使用。

---

## 元数据结构（`tools_metadata.json`）

每条记录字段如下：

```json
{
  "calc_id": "480",
  "slug": "sodium-correction-rate-hyponatremia-hypernatremia",
  "name": "工具全名",
  "url": "https://www.mdcalc.com/calc/...",
  "short_description": "一句话描述",
  "full_description": "临床建议、注意事项、管理要点",
  "function_name": "sodium_correction_rate",
  "file_path": "outputs/tools/480_sodium-correction-rate....py",
  "parameters": [
    {
      "name": "weight",
      "type": "float",
      "description": "Body weight in kg",
      "options": "Valid range: 1–300 kg"
    }
  ],
  "returns": [
    {
      "key": "fluid_rate_ml_hr",
      "type": "float",
      "description": "Recommended IV infusion rate in mL/hr"
    }
  ],
  "raises": ["ValueError: If weight is outside 1–300 kg."],
  "notes": "临床注意事项",
  "generated_code": "完整函数源码字符串"
}
```

---

## 已知情况

- 工具 **790**（Peak Expiratory Flow，NHANES III 分支）已从库中移除，原因是 NHANES III 回归系数无法从爬取数据中验证。其余 871 个工具的公式均可溯源至 MDCalc 页面数据。
- 极少数工具（3 个：10005、101、10550）的个别参数有临床合理的默认值（如 `stool_osm=290`），这是依据医学惯例填入的，文档中有说明，调用时可显式传参覆盖。
