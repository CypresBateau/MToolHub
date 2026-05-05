"""
inference.py — 图像预处理 + 单张推理后处理。

对标 Zero-shot_classification/test.py 第 341–370 行 + dataset.py 预处理。
"""
from __future__ import annotations

import io
from typing import TYPE_CHECKING

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

from .model_singleton import ORIGINAL_CLASS

if TYPE_CHECKING:
    from .model_singleton import ModelSingleton

# 与 Chexpert_Dataset / Chestxray14_Dataset 完全一致的预处理
_TRANSFORM = transforms.Compose([
    transforms.Resize([224, 224]),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
])


def _load_image_bytes(data: bytes, filename: str) -> Image.Image:
    """
    从原始字节加载 PIL.Image（RGB）。
    DICOM 文件通过 pydicom 读取并做直方图均衡化（与 RSNA_Dataset 一致）。
    """
    lower = filename.lower()
    if lower.endswith(".dcm"):
        import cv2
        import pydicom

        dcm = pydicom.dcmread(io.BytesIO(data))
        arr = dcm.pixel_array.astype(np.float32)
        # 归一化到 0-255 uint8
        arr = ((arr - arr.min()) / (arr.max() - arr.min() + 1e-8) * 255).astype(np.uint8)
        arr = cv2.equalizeHist(arr)
        img = Image.fromarray(arr).convert("RGB")
    else:
        img = Image.open(io.BytesIO(data)).convert("RGB")
    return img


def run_inference(
    image_bytes: bytes,
    filename: str,
    singleton: "ModelSingleton",
) -> list[float]:
    """
    对单张图像执行推理，返回 75 个疾病的概率列表（float，与 ORIGINAL_CLASS 顺序一致）。

    对标 test.py 第 349–370 行；feature 模式下不做 MIMIC_mapping 过滤，
    返回全部 75 个疾病的原始概率供上层按需筛选。
    """
    img = _load_image_bytes(image_bytes, filename)
    tensor = _TRANSFORM(img).unsqueeze(0).to(singleton.device)  # [1, 3, 224, 224]

    model = singleton.model
    mode = singleton.mode
    n_class = len(ORIGINAL_CLASS)

    with torch.no_grad():
        # MAVL forward 返回 (pred_class, location, concept_features, pred_global, ensemble)
        pred_class, _location, _concept_features, pred_global, _ensemble = model(tensor)

        if mode == "feature":
            # pred_class shape: [B, n_class*2] 或 [B, n_class, 2]
            pred_class = F.softmax(
                pred_class.reshape(-1, 2), dim=-1
            ).reshape(-1, n_class, 2)
            probs = pred_class[0, :, 1]                        # [75]
        else:  # text / global
            # pred_global shape: [B, N_concepts, N_disease] (raw logits)
            preds_global = []
            for normal_idx in [0, 1]:
                normal = pred_global[:, :, [normal_idx]].repeat(1, 1, n_class)
                pred_global_ = torch.stack([normal, pred_global], dim=-1)
                pred_global_ = F.softmax(pred_global_, dim=-1)
                preds_global.append(pred_global_)
            pred_global = torch.stack(preds_global, dim=0).mean(dim=0)
            probs = pred_global[0, :, :, 1].mean(dim=0)        # [75]

    return probs.cpu().tolist()
