# MAVL 医疗影像诊断模型部署指南

本指南详细说明如何在 Linux 系统上使用 Docker 部署 MAVL（Multi-Aspect Vision-Language Pre-training）胸部 X 光疾病诊断模型，并进行推理。

---

## 目录

1. [系统要求](#1-系统要求)
2. [环境搭建](#2-环境搭建)
3. [项目准备](#3-项目准备)
4. [数据准备](#4-数据准备)
5. [模型权重下载](#5-模型权重下载)
6. [配置文件修改](#6-配置文件修改)
7. [执行推理](#7-执行推理)
8. [结果说明](#8-结果说明)
9. [单张图像推理](#9-单张图像推理)
10. [常见问题](#10-常见问题)

---

## 1. 系统要求

### 硬件要求
- **GPU**: NVIDIA GPU，显存至少 8GB（推荐 12GB+）
- **内存**: 至少 16GB RAM
- **硬盘**: 至少 50GB 可用空间

### 软件要求
- **操作系统**: Linux（Ubuntu 18.04+ 或 CentOS 7+）
- **Docker**: 19.03+
- **NVIDIA Driver**: 470.x+
- **NVIDIA Container Toolkit**: 已安装

---

## 2. 环境搭建

### 2.1 安装 Docker

#### Ubuntu 系统：
```bash
# 更新包索引
sudo apt-get update

# 安装依赖
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 添加 Docker 官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 设置稳定版仓库
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# 验证安装
sudo docker run hello-world
```

#### CentOS 系统：
```bash
# 安装依赖
sudo yum install -y yum-utils

# 添加 Docker 仓库
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

# 安装 Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io

# 启动 Docker
sudo systemctl start docker 
sudo systemctl enable docker
```

### 2.2 安装 NVIDIA Container Toolkit

```bash
# 添加 NVIDIA 包仓库
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# 更新并安装
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# 重启 Docker
sudo systemctl restart docker

# 验证 GPU 支持
sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### 2.3 允许当前用户使用 Docker（可选）

```bash
# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER

# 重新登录或执行
newgrp docker

# 验证（不需要 sudo）
docker run hello-world
```

---

## 3. 项目准备

### 3.1 下载项目代码

```bash
# 克隆项目（如果从 GitHub）
git clone https://github.com/your-repo/MAVL.git
cd MAVL

# 或者如果已在 Windows 上下载，通过 scp 传输到 Linux
# 在 Windows 上执行：
# scp -r MAVL user@linux-server:/path/to/destination/
```

### 3.2 准备数据目录结构

```bash
# 创建数据根目录
sudo mkdir -p /data/MAVL
sudo chown -R $USER:$USER /data/MAVL

# 推荐的目录结构
/data/MAVL/
├── checkpoints/           # 存放模型权重
├── data/                  # 存放数据集
│   ├── chexpert/
│   ├── chestxray14/
│   └── ...
└── results/               # 存放推理结果
```

---

## 4. 数据准备

### 4.1 理解数据输入格式

MAVL 模型需要以下输入：

#### 必需文件：

1. **医学图像文件**
   - 格式：JPG、PNG 或 DICOM（.dcm）
   - 要求：RGB 格式，将被自动调整为 224×224 像素

2. **CSV 标注文件**
   - 包含图像路径和疾病标签
   - 不同数据集有不同格式要求

### 4.2 CheXpert 数据集格式示例（推荐入门）

CSV 文件格式（`filter_test_labels.csv`）：

```csv
Path,Enlarged Cardiomediastinum,Cardiomegaly,Lung Opacity,Lung Lesion,Edema,Consolidation,Pneumonia,Atelectasis,Pneumothorax,Pleural Effusion,Pleural Other,Fracture,Support Devices
views/frontal/labeled/00000001.jpg,0,0,0,0,0,0,0,0,0,0,0,0,0
views/frontal/labeled/00000002.jpg,1,0,1,0,0,0,0,0,0,1,0,0,1
```

**关键说明：**
- 第 1 列：图像相对路径（相对于 root 目录）
- 第 2 列开始：各种疾病的标签
  - `0`: 阴性（不存在该疾病）
  - `1`: 阳性（存在该疾病）
  - `-1`: 不确定
  - `2`: 排除（不用于评估）

### 4.3 自定义数据准备（单张或多张图像）

如果您想对自己的图像进行推理，需要准备一个简单的 CSV 文件：

**步骤 1：组织图像文件**

```bash
# 假设您的图像放在：
/data/MAVL/my_data/images/
├── patient001.jpg
├── patient002.jpg
└── patient003.jpg
```

**步骤 2：创建 CSV 文件**

创建 `/data/MAVL/my_data/test_labels.csv`：

```csv
image_path,Enlarged Cardiomediastinum,Cardiomegaly,Lung Opacity,Lung Lesion,Edema,Consolidation,Pneumonia,Atelectasis,Pneumothorax,Pleural Effusion,Pleural Other,Fracture,Support Devices
patient001.jpg,0,0,0,0,0,0,0,0,0,0,0,0,0
patient002.jpg,0,0,0,0,0,0,0,0,0,0,0,0,0
patient003.jpg,0,0,0,0,0,0,0,0,0,0,0,0,0
```

**注意：**
- 如果您不确定标签，可以全部填 `0` 或 `-1`
- 推理结果主要依赖模型预测，标签仅用于评估（如果有真实标签）

### 4.4 支持的 DICOM 格式（RSNA 数据集）

对于 DICOM 文件（.dcm），模型会自动处理：
- 使用 pydicom 读取
- 自动进行直方图均衡化
- 转换为 RGB 格式

```bash
# DICOM 文件结构示例
/data/MAVL/rsna/data/
├── 000001.dcm
├── 000002.dcm
└── ...
```

---

## 5. 模型权重下载

### 5.1 下载预训练模型

#### 方法 1：使用 gdown（推荐）

```bash
# 安装 gdown
pip install gdown

# 下载模型权重（根据文档中的 Google Drive 链接）
# 示例：下载 checkpoint_full_46.pth（最佳零样本分类模型）
cd /data/MAVL/checkpoints
gdown <Google Drive ID>

# 或者从项目提供的下载链接
# 查看 Pretrain/data_file/DATA_Prepare.md 获取最新链接
```

#### 方法 2：直接从 Docker 镜像获取

```bash
# 拉取预配置的 Docker 镜像
docker pull stevephan46/mavl:latest

# 启动容器并复制模型文件
docker run --name mavl_temp stevephan46/mavl:latest ls /workspace/MAVL/checkpoints/
docker cp mavl_temp:/workspace/MAVL/checkpoints/checkpoint_full_46.pth /data/MAVL/checkpoints/
docker rm mavl_temp
```

### 5.2 验证模型文件

```bash
# 检查文件大小（约 300-500MB）

ls -lh /data/MAVL/checkpoints/checkpoint_full_46.pth

# 使用 Python 验证 checkpoint 结构
python3 << EOF
import torch
ckpt = torch.load('/data/MAVL/checkpoints/checkpoint_full_46.pth', map_location='cpu')
print("Checkpoint keys:", ckpt.keys())
print("Model state_dict keys (first 5):", list(ckpt['model'].keys())[:5])
EOF
```

---

## 6. 配置文件修改

### 6.1 复制并修改配置文件

```bash
# 进入推理目录
cd /path/to/MAVL/Zero-shot_classification

# 复制示例配置
cp configs/chexp     ert_mavl.yaml configs/my_data_mavl.yaml
```

### 6.2 编辑配置文件

使用文本编辑器修改 `configs/my_data_mavl.yaml`：

```yaml
# ==========================================
# 数据路径配置（必须修改）
# ==========================================

# CSV 标注文件路径（绝对路径）
test_file: '/data/MAVL/my_data/test_labels.csv'

# 数据根目录（图像文件的父目录）
root: '/data/MAVL/my_data'

# 模型权重路径
model_path: '/data/MAVL/checkpoints/checkpoint_full_46.pth'

# ==========================================
# 书籍文件路径（相对路径即可）
# ==========================================

# 疾病描述文件
disease_book: 'observation explanation.json'

# GPT-4 生成的概念文件（相对于 Zero-shot_classification 目录）
concept_book: '../Pretrain/concept_gen/gpt4_mimic.json'

# ==========================================
# 数据集配置
# ==========================================

# 数据集类型：chexpert, chestxray14, padchest, rsna, siim 等
dataset: 'chexpert'

# ==========================================
# 模型配置（通常不需要修改）
# ==========================================

model: 'mavl'                    # 使用 MAVL 模型
base_model: 'resnet50'           # 视觉编码器
d_model: 256                     # 特征维度
decoder: cross                   # 解码器类型
num_queries: 75                  # 疾病数量
dropout: 0.1
attribute_set_size: 2            # 二分类（存在/不存在）
N: 4                             # Transformer 层数
H: 4                             # 注意力头数
text_encoder: 'emilyalsentzer/Bio_ClinicalBERT'
self_attention: True
pretrained: True

# ==========================================
# 推理配置
# ==========================================

# 推理模式
# - feature: 使用局部特征分类（推荐，准确率更高）
# - text: 使用全局文本特征分类
mode: feature

# 图像分辨率
image_res: 224

# 批量大小（根据 GPU 显存调整）
# - 8GB 显存: 64-128
# - 12GB 显存: 128-256
# - 16GB+ 显存: 256-512
test_batch_size: 128

# CheXpert 特定配置
chexpert_subset: True            # 使用 5 类子集
```

### 6.3 配置文件路径说明

```
MAVL/
├── Pretrain/
│   └── concept_gen/
│       └── gpt4_mimic.json          # GPT-4 概念文件
└── Zero-shot_classification/
    ├── configs/
    │   └── my_data_mavl.yaml        # 您的配置文件
    ├── observation explanation.json  # 疾病描述文件
    └── test.py                       # 推理脚本
```

---

## 7. 执行推理

### 7.1 使用 Docker 运行（推荐）

#### 方法 1：交互式容器

```bash
# 启动容器并挂载数据目录
docker run --runtime=nvidia --name mavl_inference \
    -it \
    -v /data/MAVL:/data/MAVL \
    -v /path/to/MAVL:/workspace/MAVL \
    --shm-size=4g \
    stevephan46/mavl:latest

# 容器启动后，执行推理
cd /workspace/MAVL/Zero-shot_classification
python test.py --config configs/my_data_mavl.yaml
```

#### 方法 2：单次运行（适合脚本化）

```bash
docker run --runtime=nvidia \
    -v /data/MAVL:/data/MAVL \
    -v /path/to/MAVL:/workspace/MAVL \
    --shm-size=4g \
    stevephan46/mavl:latest \
    bash -c "cd /workspace/MAVL/Zero-shot_classification && python test.py --config configs/my_data_mavl.yaml"
```

#### 方法 3：构建自定义 Docker 镜像

如果预构建镜像不满足需求：

```bash
# 在项目根目录
cd /path/to/MAVL

# 构建 Docker 镜像
docker build -t mavl:custom .

# 运行自定义镜像
docker run --runtime=nvidia \
    -it \
    -v /data/MAVL:/data/MAVL \
    --shm-size=4g \
    mavl:custom
```

### 7.2 直接在 Linux 上运行（不使用 Docker）

#### 步骤 1：创建 Python 虚拟环境

```bash
# Python 3.8+ 推荐
python3.8 -m venv /data/MAVL/venv
source /data/MAVL/venv/bin/activate
```

#### 步骤 2：安装依赖

```bash
cd /path/to/MAVL

# 安装 PyTorch（根据您的 CUDA 版本调整）
pip install torch==1.12.0+cu113 torchvision==0.13.0+cu113 torchaudio==0.12.0 --extra-index-url https://download.pytorch.org/whl/cu113

# 安装其他依赖
pip install -r requirements.txt

# 安装 opencv-python（特定版本）
pip install opencv-python==4.2.0.32
```

#### 步骤 3：执行推理

```bash
cd Zero-shot_classification

# 激活虚拟环境
source /data/MAVL/venv/bin/activate

# 运行推理
python test.py --config configs/my_data_mavl.yaml
```

### 7.3 指定 GPU 运行

```bash
# 使用第一块 GPU
CUDA_VISIBLE_DEVICES=0 python test.py --config configs/my_data_mavl.yaml

# 使用多块 GPU
CUDA_VISIBLE_DEVICES=0,1 python test.py --config configs/my_data_mavl.yaml
```

---

## 8. 结果说明

### 8.1 控制台输出

推理完成后，会在终端输出结果表格：

```
+------------------------+------------+---------+----------+-----------+--------+
| Class Name             | Accuracy   | Max F1  | AUC ROC  | Precision | Recall |
+------------------------+------------+---------+----------+-----------+--------+
| Enlarged Cardiomediastinum | 0.920  | 0.456   | 0.856    | 0.352     | 0.682  |
| Cardiomegaly           | 0.830      | 0.756   | 0.906    | 0.674     | 0.861  |
| Lung Opacity           | 0.768      | 0.623   | 0.834    | 0.589     | 0.667  |
| Lung Lesion            | 0.889      | 0.234   | 0.723    | 0.156     | 0.456  |
| Edema                  | 0.868      | 0.663   | 0.927    | 0.557     | 0.821  |
| Consolidation          | 0.901      | 0.445   | 0.812    | 0.334     | 0.678  |
| Pneumonia              | 0.912      | 0.523   | 0.856    | 0.423     | 0.701  |
| Atelectasis            | 0.823      | 0.567   | 0.845    | 0.478     | 0.701  |
| Pneumothorax           | 0.956      | 0.612   | 0.892    | 0.523     | 0.745  |
| Pleural Effusion       | 0.801      | 0.701   | 0.889    | 0.623     | 0.801  |
+------------------------+------------+---------+----------+-----------+--------+
| Average                | 0.864      | 0.688   | 0.913    | 0.616     | 0.787  |
+------------------------+------------+---------+----------+-----------+--------+
```

**指标说明：**
- **Accuracy**: 准确率（使用最佳 F1 阈值）
- **Max F1**: 最大 F1 分数
- **AUC ROC**: ROC 曲线下面积（最重要指标）
- **Precision**: 精确率
- **Recall**: 召回率

### 8.2 保存的文件

推理结果会保存在两个位置：

#### 1. 详细结果文件（当前目录）

文件名：`result_{model}_{dataset}_{mode}.csv`

例如：`result_mavl_my_data_feature.csv`

```csv
Class Name,Accuracy,Max F1,AUC ROC,Precision,Recall
Enlarged Cardiomediastinum,0.92,0.456,0.856,0.352,0.682
Cardiomegaly,0.83,0.756,0.906,0.674,0.861
...
Average,0.864,0.688,0.913,0.616,0.787
```

#### 2. 汇总结果文件

路径：`results/{model_name}.csv`

```csv
Dataset,Accuracy,Max F1,AUC ROC,Precision,Recall
my_data_feature,0.864,0.688,0.913,0.616,0.787
```

### 8.3 获取每张图像的预测概率

默认代码只输出整体评估指标。如需获取每张图像的预测概率，请参考下一节。

---

## 9. 单张图像推理

默认代码只支持批量推理。以下提供三种方法进行单张图像推理。

### 9.1 方法 1：创建单图 CSV 文件（最简单）

**步骤：**

1. 创建 CSV 文件 `single_image.csv`：
```csv
image_path,Enlarged Cardiomediastinum,Cardiomegaly,Lung Opacity,Lung Lesion,Edema,Consolidation,Pneumonia,Atelectasis,Pneumothorax,Pleural Effusion,Pleural Other,Fracture,Support Devices
patient001.jpg,0,0,0,0,0,0,0,0,0,0,0,0,0
```

2. 将图像放在相应位置
3. 运行推理（batch_size 设为 1）

### 9.2 方法 2：修改 test.py 保存预测概率

在 `Zero-shot_classification/test.py` 中找到推理循环部分（约 338-370 行），添加保存代码：

```python
# 在 test 函数中，pred 列表收集完成后（约 370 行）
# 添加以下代码保存每张图像的预测概率

import pandas as pd

# 获取所有预测概率
pred_np = torch.cat(pred, dim=0).cpu().numpy()  # [N, n_diseases]

# 获取图像路径
img_paths = []
for sample in test_dataloader:
    if 'img_path' in sample:
        img_paths.extend(sample['img_path'])

# 保存预测结果
results_df = pd.DataFrame(pred_np, columns=target_class)
results_df.insert(0, 'image_path', img_paths)
results_df.to_csv('predictions_per_image.csv', index=False)
print(f"已保存每张图像的预���概率到 predictions_per_image.csv")
```

### 9.3 方法 3：使用独立推理脚本

创建新文件 `infer_single_image.py`：

```python
#!/usr/bin/env python3
"""
MAVL 单张图像推理脚本
使用方法：
    python infer_single_image.py --image /path/to/image.jpg --config configs/chexpert_mavl.yaml
"""

import os
import yaml
import torch
import argparse
from PIL import Image
from torchvision import transforms
import pandas as pd
from models.model_MAVL import MAVL
from transformers import BertTokenizer

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True, help='输入图像路径')
    parser.add_argument('--config', type=str, required=True, help='配置文件路径')
    parser.add_argument('--checkpoint', type=str, help='模型权重路径（覆盖配置文件）')
    parser.add_argument('--output', type=str, default='prediction_result.csv', help='输出文件路径')
    return parser.parse_args()

def load_config(config_path):
    """加载配置文件"""
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.Loader)
    return config

def get_class_labels(dataset):
    """根据数据集返回疾病标签"""
    if dataset == 'chexpert':
        return ['Enlarged Cardiomediastinum', 'Cardiomegaly', 'Lung Opacity',
                'Lung Lesion', 'Edema', 'Consolidation', 'Pneumonia',
                'Atelectasis', 'Pneumothorax', 'Pleural Effusion',
                'Pleural Other', 'Fracture', 'Support Devices']
    # 添加其他数据集...
    return []

def load_image(image_path, image_res=224):
    """加载并预处理图像"""
    normalize = transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    transform = transforms.Compose([
        transforms.Resize([image_res, image_res]),
        transforms.ToTensor(),
        normalize,
    ])

    img = Image.open(image_path).convert('RGB')
    img_tensor = transform(img).unsqueeze(0)  # [1, 3, 224, 224]
    return img_tensor

def load_model(config):
    """加载模型"""
    # 初始化 tokenizer
    tokenizer = BertTokenizer.from_pretrained(config['text_encoder'])

    # 加载文本书籍（简化版，实际需要完整加载）
    # 这里假设您有完整的文本加载逻辑
    # 参考 test.py 中的 load_books 函数

    # 创建模型
    model = MAVL(
        config=config,
        ana_book_tokenizer=None,  # 需要正确加载
        disease_book_tokenizer=None,
        concepts_book_tokenizer=None
    )

    # 加载权重
    checkpoint_path = config['model_path']
    print(f"加载模型权重: {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    state_dict = checkpoint['model']
    state_dict = {k.replace('module.', ''): v for k, v in state_dict.items()}
    state_dict = {k: v for k, v in state_dict.items() if 'temp' not in k}
    model.load_state_dict(state_dict)

    return model, tokenizer

def infer(model, image_tensor, config, device='cuda'):
    """执行推理"""
    model.eval()
    model.to(device)
    image_tensor = image_tensor.to(device)

    with torch.no_grad():
        if config['model'] == 'mavl':
            pred_class, location, concept_features, pred_global, ensemble = model(image_tensor)

            # 处理预测结果
            import torch.nn.functional as F
            pred_class = F.softmax(pred_class.reshape(-1, 2)).reshape(1, -1, 2)
            pred_prob = pred_class[0, :, 1].cpu().numpy()  # 取正类概率
        else:
            raise ValueError(f"未知模型类型: {config['model']}")

    return pred_prob

def main():
    args = parse_args()

    # 加载配置
    config = load_config(args.config)
    if args.checkpoint:
        config['model_path'] = args.checkpoint

    # 检查图像文件
    if not os.path.exists(args.image):
        print(f"错误: 图像文件不存在: {args.image}")
        return

    # 设置设备
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"使用设备: {device}")

    # 加载模型（需要完善文本加载部分）
    # model, tokenizer = load_model(config)
    print("注意: 此脚本需要完整的文本加载逻辑，请参考 test.py 完善")
    print("建议使用方法 1 或方法 2 进行单张图像推理")

    # 加载图像
    # image_tensor = load_image(args.image, config['image_res'])

    # 推理
    # predictions = infer(model, image_tensor, config, device)

    # 获取标签
    # class_labels = get_class_labels(config['dataset'])

    # 保存结果
    # results_df = pd.DataFrame({
    #     'class': class_labels,
    #     'probability': predictions
    # })
    # results_df = results_df.sort_values('probability', ascending=False)
    # results_df.to_csv(args.output, index=False)
    # print(f"\n推理结果已保存到: {args.output}")
    # print(results_df.to_string(index=False))

if __name__ == '__main__':
    main()
```

**推荐：使用方法 2（修改 test.py）**
这是最简单可靠的方法，只需要在现有代码基础上添加几行保存逻辑。

---

## 10. 常见问题

### 10.1 Docker 相关问题

**Q: docker: command not found**
```bash
# 检查 Docker 是否安装
docker --version

# 重新安装（参考 2.1 节）
```

**Q: docker: Got permission denied**
```bash
# 方案 1：使用 sudo
sudo docker run ...

# 方案 2：将用户添加到 docker 组
sudo usermod -aG docker $USER
newgrp docker
```

**Q: nvidia-container-toolkit 无法访问 GPU**
```bash
# 检查 NVIDIA 驱动
nvidia-smi

# 重新安装 nvidia-container-toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# 测试
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### 10.2 推理相关问题

**Q: CUDA out of memory**
```bash
# 减小 batch_size
# 在配置文件中设置：
test_batch_size: 32  # 或更小

# 或使用 CPU（慢）
CUDA_VISIBLE_DEVICES="" python test.py --config configs/my_data.yaml
```

**Q: 找不到模型文件**
```bash
# 检查文件是否存在
ls -lh /data/MAVL/checkpoints/checkpoint_full_46.pth

# 检查配置文件中的路径是否为绝对路径
cat configs/my_data_mavl.yaml | grep model_path
```

**Q: 图像加载失败**
```bash
# 检查图像格式
file /data/MAVL/my_data/patient001.jpg

# 检查 CSV 中的路径是否正确
cat /data/MAVL/my_data/test_labels.csv

# 确保图像是 RGB 格式
# 如果是灰度图，代码会自动转换
```

**Q: ImportError: No module named 'xxx'**
```bash
# 激活虚拟环境
source /data/MAVL/venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt

# Docker 环境中
docker exec -it mavl_container pip install missing_package
```

### 10.3 性能优化

**Q: 推理速度慢**

```bash
# 1. 增加 batch_size（在显存允许范围内）
test_batch_size: 256  # 或更大

# 2. 使用混合精度推理
# 修改 test.py，在推理前添加：
from torch.cuda.amp import autocast
with autocast():
    pred_class = model(input_image)

# 3. 预加载图像到内存
# 修改 Dataset 类，在 __init__ 中预加载
```

**Q: 多 GPU 推理**

```bash
# 使用 accelerate
accelerate launch --multi_gpu --num_processes=2 test.py --config configs/my_data.yaml

# 或设置 CUDA_VISIBLE_DEVICES
CUDA_VISIBLE_DEVICES=0,1 python test.py --config configs/my_data.yaml
```

### 10.4 数据格式问题

**Q: CSV 格式错误**
```bash
# 检查 CSV 格式
python3 << EOF
import pandas as pd
df = pd.read_csv('/data/MAVL/my_data/test_labels.csv')
print("列名:", df.columns.tolist())
print("形状:", df.shape)
print(df.head())
EOF

# 确保使用 UTF-8 编码
iconv -f GBK -t UTF-8 input.csv > output.csv
```

**Q: DICOM 文件读取失败**
```bash
# 安装 pydicom
pip install pydicom

# 测试读取
python3 << EOF
import pydicom
import matplotlib.pyplot as plt

dcm = pydicom.read_file('/path/to/file.dcm')
print("图像形状:", dcm.pixel_array.shape)
plt.imshow(dcm.pixel_array, cmap='gray')
plt.savefig('test_dicom.png')
EOF
```

---

## 11. 完整部署示例（从零开始）

以下是一个从零开始的完整部署流程示例：

```bash
# ============================================
# 步骤 1: 环境准备（Ubuntu 20.04）
# ============================================

# 安装 Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# 安装 NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# 验证 GPU 支持
sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# ============================================
# 步骤 2: 下载项目
# ============================================

cd /opt
git clone https://github.com/your-repo/MAVL.git
cd MAVL

# ============================================
# 步骤 3: 准备数据和模型
# ============================================

# 创建目录结构
sudo mkdir -p /data/MAVL/{checkpoints,data/my_data,results}
sudo chown -R $USER:$USER /data/MAVL

# 下载模型（替换为实际的下载链接）
cd /data/MAVL/checkpoints
wget https://example.com/checkpoint_full_46.pth
# 或使用 gdown
# gdown <Google Drive ID>

# ============================================
# 步骤 4: 准备测试数据
# ============================================

# 假设您的图像在 /data/MAVL/data/my_data/images/
# 创建 CSV 文件
cat > /data/MAVL/data/my_data/test_labels.csv << EOF
image_path,Enlarged Cardiomediastinum,Cardiomegaly,Lung Opacity,Lung Lesion,Edema,Consolidation,Pneumonia,Atelectasis,Pneumothorax,Pleural Effusion,Pleural Other,Fracture,Support Devices
patient001.jpg,0,0,0,0,0,0,0,0,0,0,0,0,0
patient002.jpg,0,0,0,0,0,0,0,0,0,0,0,0,0
EOF

# ============================================
# 步骤 5: 创建配置文件
# ============================================

cd /opt/MAVL/Zero-shot_classification

cat > configs/my_data_mavl.yaml << EOF
test_file: '/data/MAVL/data/my_data/test_labels.csv'
disease_book: 'observation explanation.json'
concept_book: '../Pretrain/concept_gen/gpt4_mimic.json'
dataset: 'chexpert'
root: '/data/MAVL/data/my_data'
model: 'mavl'
model_path: '/data/MAVL/checkpoints/checkpoint_full_46.pth'
mode: feature
image_res: 224
test_batch_size: 64
d_model: 256
base_model: 'resnet50'
decoder: cross
num_queries: 75
dropout: 0.1
attribute_set_size: 2
N: 4
H: 4
text_encoder: 'emilyalsentzer/Bio_ClinicalBERT'
self_attention: True
pretrained: True
chexpert_subset: True
EOF

# ============================================
# 步骤 6: 运行推理
# ============================================

# 方法 1: 使用 Docker
docker run --runtime=nvidia \
    -v /data/MAVL:/data/MAVL \
    -v /opt/MAVL:/workspace/MAVL \
    --shm-size=4g \
    stevephan46/mavl:latest \
    bash -c "cd /workspace/MAVL/Zero-shot_classification && python test.py --config configs/my_data_mavl.yaml"

# 方法 2: 不使用 Docker（需先安装依赖）
# python3.8 -m venv /data/MAVL/venv
# source /data/MAVL/venv/bin/activate
# pip install torch==1.12.0+cu113 torchvision==0.13.0+cu113 --extra-index-url https://download.pytorch.org/whl/cu113
# pip install -r requirements.txt
# python test.py --config configs/my_data_mavl.yaml

# ============================================
# 步骤 7: 查看结果
# ============================================

# 结果文件
ls -lh result_*.csv
cat result_mavl_my_data_feature.csv

# 汇总结果
cat results/mavl.csv
```

---

## 12. 总结

本指南涵盖了 MAVL 模型在 Linux Docker 环境下的完整部署流程：

1. ✅ **环境搭建**: Docker + NVIDIA GPU 支持
2. ✅ **数据准备**: 图像和 CSV 格式要求
3. ✅ **模型下载**: checkpoint 获取方法
4. ✅ **配置修改**: YAML 配置文件详解
5. ✅ **推理执行**: Docker 和本地两种方式
6. ✅ **结果输出**: 评估指标和预测概率
7. ✅ **单图推理**: 三种方法实现
8. ✅ **问题解决**: 常见问题排查

**关键要点：**
- 使用 Docker 可以避免环境配置问题
- CSV 文件格式必须正确（第一列为图像路径）
- 根据显存调整 `test_batch_size`
- `checkpoint_full_46.pth` 适用于分类任务
- 结果包括 AUC-ROC、F1、Accuracy 等指标

如有问题，请参考原始论文或项目 GitHub 页面。

---

**论文引用：**
```
@inproceedings{phan2024decomposing,
  title={Decomposing Disease Descriptions for Enhanced Pathology Detection: A Multi-Aspect Vision-Language Pre-training Framework},
  author={Phan, Vu Minh Hieu and Xie, Yutong and Qi, Yuankai and Liu, Lingqiao and Liu, Liyang and Zhang, Bowen and Liao, Zhibin and Wu, Qi and To, Minh-Son and Verjans, Johan W},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={11492--11501},
  year={2024}
}
```
