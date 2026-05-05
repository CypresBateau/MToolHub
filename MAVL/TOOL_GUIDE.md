# MAVL 工具说明

MAVL（Multi-dimensional Visual and Language，CVPR 2024）用于胸部 X 光片的零样本多标签分类。
通过 Gateway 统一调用，地址：`POST http://<服务器IP>:9000/tools/mavl/predict`

---

## 输入

| 项目 | 说明 |
|---|---|
| 文件格式 | `.jpg` `.jpeg` `.png` `.dcm`（DICOM） |
| 文件大小 | ≤ 20MB |
| 图像内容 | 胸部正位/侧位 X 光片 |
| 预处理 | 自动缩放至 224×224，无需手动处理 |

---

## 输出

返回 **75 种放射学类别**的概率分布（0–1）。

**关键字段：**

| 字段 | 说明 |
|---|---|
| `predictions` | 全部 75 种类别概率，顺序固定 |
| `top_k` | 概率最高的 K 个类别，按降序排列 |
| `inference_time_ms` | 纯推理耗时（毫秒） |

**调用示例：**

```bash
curl -X POST http://localhost:9000/tools/mavl/predict \
  -F "file=@chest_xray.jpg" \
  -F "top_k=5" \
  | python3 -m json.tool
```

```python
import requests

resp = requests.post(
    "http://localhost:9000/tools/mavl/predict",
    files={"file": ("xray.jpg", open("chest_xray.jpg", "rb"), "image/jpeg")},
    data={"top_k": 5},
)
result = resp.json()

# 只看临床关键类别
CLINICAL = {"effusion","pneumothorax","edema","atelectasis",
            "consolidation","pneumonia","cardiomegaly","nodule","mass","fracture"}
clinical = [p for p in result["predictions"] if p["disease"] in CLINICAL]
clinical.sort(key=lambda x: x["probability"], reverse=True)
for item in clinical:
    print(f"{item['disease']}: {item['probability']:.4f}")
```

---

## 临床重点类别

75 个类别中包含放射报告描述性词汇（如 `normal`、`stable`、`tortuous`），
临床应用时通常只关注以下类别：

| 类别 | 中文 |
|---|---|
| `effusion` | 胸腔积液 |
| `pneumothorax` | 气胸 |
| `edema` | 肺水肿 |
| `atelectasis` | 肺不张 |
| `consolidation` | 实变 |
| `pneumonia` | 肺炎 |
| `cardiomegaly` | 心脏扩大 |
| `nodule` | 结节 |
| `mass` | 肿块 |
| `fracture` | 骨折 |

---

## 75 种类别完整列表（predictions 顺序）

```
normal, clear, sharp, sharply, unremarkable, intact, stable, free,
effusion, opacity, pneumothorax, edema, atelectasis, tube, consolidation,
process, abnormality, enlarge, tip, low, pneumonia, line, congestion,
catheter, cardiomegaly, fracture, air, tortuous, lead, disease,
calcification, prominence, device, engorgement, picc, clip, elevation,
expand, nodule, wire, fluid, degenerative, pacemaker, thicken, marking,
scar, hyperinflate, blunt, loss, widen, collapse, density, emphysema,
aerate, mass, crowd, infiltrate, obscure, deformity, hernia, drainage,
distention, shift, stent, pressure, lesion, finding, borderline,
hardware, dilation, chf, redistribution, aspiration,
tail_abnorm_obs, excluded_obs
```

---

## 模型信息

| 项目 | 值 |
|---|---|
| 论文 | MAVL, CVPR 2024 |
| 视觉编码器 | ResNet-50 |
| 文本编码器 | Bio_ClinicalBERT |
| Checkpoint | `checkpoint_full_46.pth` |
| GPU 显存占用 | ~400MB |
| 首次加载时间 | ~20–30 秒 |
| 推理耗时 | ~50ms/张 |
