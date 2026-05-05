"""
model_singleton.py — 启动时加载一次 MAVL 模型，全局复用。

对标 Zero-shot_classification/test.py 第 276–329 行。
不修改原始代码，通过 sys.path.insert 复用 Zero-shot_classification/models/。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import torch

# ── 路径注入：让 Python 能 import Zero-shot_classification 里的模块 ─────────
REPO_ROOT = Path(__file__).resolve().parents[2]          # .../MAVL/
ZSC_PATH = str(REPO_ROOT / "Zero-shot_classification")
if ZSC_PATH not in sys.path:
    sys.path.insert(0, ZSC_PATH)

from models.model_MAVL import MAVL                        # noqa: E402
from models.tokenization_bert import BertTokenizer        # noqa: E402

# ── 75 个 original_class（与 test.py 181–189 行完全一致）─────────────────────
ORIGINAL_CLASS: list[str] = [
    'normal', 'clear', 'sharp', 'sharply', 'unremarkable', 'intact', 'stable', 'free',
    'effusion', 'opacity', 'pneumothorax', 'edema', 'atelectasis', 'tube', 'consolidation',
    'process', 'abnormality', 'enlarge', 'tip', 'low',
    'pneumonia', 'line', 'congestion', 'catheter', 'cardiomegaly', 'fracture', 'air',
    'tortuous', 'lead', 'disease', 'calcification', 'prominence',
    'device', 'engorgement', 'picc', 'clip', 'elevation', 'expand', 'nodule', 'wire',
    'fluid', 'degenerative', 'pacemaker', 'thicken', 'marking', 'scar',
    'hyperinflate', 'blunt', 'loss', 'widen', 'collapse', 'density', 'emphysema',
    'aerate', 'mass', 'crowd', 'infiltrate', 'obscure', 'deformity', 'hernia',
    'drainage', 'distention', 'shift', 'stent', 'pressure', 'lesion', 'finding',
    'borderline', 'hardware', 'dilation', 'chf', 'redistribution', 'aspiration',
    'tail_abnorm_obs', 'excluded_obs',
]

# ── 51 个解剖位置（与 test.py 279–292 行完全一致）────────────────────────────
ANA_LOCATIONS: list[str] = [
    'trachea', 'left_hilar', 'right_hilar', 'hilar_unspec', 'left_pleural',
    'right_pleural', 'pleural_unspec', 'heart_size', 'heart_border', 'left_diaphragm',
    'right_diaphragm', 'diaphragm_unspec', 'retrocardiac', 'lower_left_lobe',
    'upper_left_lobe', 'lower_right_lobe', 'middle_right_lobe', 'upper_right_lobe',
    'left_lower_lung', 'left_mid_lung', 'left_upper_lung', 'left_apical_lung',
    'left_lung_unspec', 'right_lower_lung', 'right_mid_lung', 'right_upper_lung',
    'right_apical_lung', 'right_lung_unspec', 'lung_apices', 'lung_bases',
    'left_costophrenic', 'right_costophrenic', 'costophrenic_unspec',
    'cardiophrenic_sulcus', 'mediastinal', 'spine', 'clavicle', 'rib', 'stomach',
    'right_atrium', 'right_ventricle', 'aorta', 'svc', 'interstitium', 'parenchymal',
    'cavoatrial_junction', 'cardiopulmonary', 'pulmonary', 'lung_volumes',
    'unspecified', 'other',
]

# ── 模型默认配置（与 chexpert_mavl.yaml 一致）────────────────────────────────
DEFAULT_MODEL_CONFIG: dict[str, Any] = {
    "d_model": 256,
    "base_model": "resnet50",
    "decoder": "cross",
    "num_queries": 75,
    "dropout": 0.1,
    "attribute_set_size": 2,
    "N": 4,
    "H": 4,
    "self_attention": True,
    "pretrained": False,   # serving 时不再从 ImageNet 重新下载，权重已在 checkpoint 里
    "image_res": 224,
}


def _get_tokenizer(tokenizer: BertTokenizer, texts: list[str]) -> Any:
    """对标 test.py get_tokenizer（第 143–146 行）。"""
    return tokenizer(
        texts,
        padding="max_length",
        truncation=True,
        max_length=64,
        return_tensors="pt",
    )


class ModelSingleton:
    """持有加载后的模型及相关 tokenizer，进程内单例。"""

    _instance: "ModelSingleton | None" = None

    def __init__(self) -> None:
        self.model: MAVL | None = None
        self.device: torch.device | None = None
        self.disease_book_tokenizer: Any = None
        self.ana_book_tokenizer: Any = None
        self.concepts_book_tokenizer: Any = None
        self.checkpoint_name: str = ""
        self.mode: str = "feature"
        self.loaded: bool = False

    @classmethod
    def get(cls) -> "ModelSingleton":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load(self) -> None:
        """读取环境变量，初始化模型（应在 lifespan 启动钩子中调用一次）。"""
        model_path = os.environ["MAVL_MODEL_PATH"]
        disease_book_path = os.environ["MAVL_DISEASE_BOOK_PATH"]
        concept_book_path = os.environ["MAVL_CONCEPT_BOOK_PATH"]
        text_encoder = os.environ["MAVL_TEXT_ENCODER"]
        device_str = os.environ.get("MAVL_DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
        self.mode = os.environ.get("MAVL_INFERENCE_MODE", "feature")

        self.device = torch.device(device_str)
        self.checkpoint_name = Path(model_path).name

        print(f"[ModelSingleton] Loading disease book from: {disease_book_path}")
        json_book = json.load(open(disease_book_path, "r"))
        disease_book = [json_book[c] for c in ORIGINAL_CLASS]
        ana_book = ["It is located at " + loc for loc in ANA_LOCATIONS]

        print(f"[ModelSingleton] Loading tokenizer: {text_encoder}")
        tokenizer = BertTokenizer.from_pretrained(text_encoder)
        self.disease_book_tokenizer = _get_tokenizer(tokenizer, disease_book).to(self.device)
        self.ana_book_tokenizer = _get_tokenizer(tokenizer, ana_book).to(self.device)

        print(f"[ModelSingleton] Loading concept book from: {concept_book_path}")
        concepts_raw = json.load(open(concept_book_path, "r"))
        concepts = {c: concepts_raw[c] for c in ORIGINAL_CLASS}
        concepts_book = sum(concepts.values(), [])
        self.concepts_book_tokenizer = _get_tokenizer(tokenizer, concepts_book).to(self.device)

        print("[ModelSingleton] Building MAVL model")
        model_config = {**DEFAULT_MODEL_CONFIG, "text_encoder": text_encoder}
        self.model = MAVL(
            model_config,
            self.ana_book_tokenizer,
            self.disease_book_tokenizer,
            self.concepts_book_tokenizer,
        )

        print(f"[ModelSingleton] Loading checkpoint: {model_path}")
        checkpoint = torch.load(model_path, map_location="cpu")
        state_dict = checkpoint["model"]
        state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}
        state_dict = {k: v for k, v in state_dict.items() if "temp" not in k}
        self.model.load_state_dict(state_dict)

        self.model.eval()
        self.model.to(self.device)
        self.loaded = True
        print(f"[ModelSingleton] Model loaded successfully on {self.device} (mode={self.mode})")
