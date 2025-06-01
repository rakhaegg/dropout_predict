from albumentations import (
    Compose, OneOf, RandomRotate90, HorizontalFlip, VerticalFlip,
    RandomBrightnessContrast, Blur, CLAHE, ShiftScaleRotate
)
from albumentations.pytorch import ToTensorV2  # utk DataLoader nanti
import cv2
import numpy as np
from typing import Dict, Any

AUG_SEED = 42   # reproducible

def get_train_transforms(size: int = 128) -> Compose:
    return Compose(
        [
            ShiftScaleRotate(
                shift_limit=0.05, scale_limit=0.05, rotate_limit=15,
                border_mode=cv2.BORDER_REFLECT_101, p=0.7),
            OneOf([
                Blur(blur_limit=3, p=0.3),
                CLAHE(clip_limit=2, p=0.7),
            ], p=0.3),
            HorizontalFlip(p=0.5),
            VerticalFlip(p=0.1),
            RandomBrightnessContrast(0.2, 0.2, p=0.5),
        ],
        additional_targets={},
        p=1.0
    )

def get_val_transforms(size: int = 128) -> Compose:
    # hanya resize & normalisasi ringan
    return Compose([], p=1.0)

def apply_aug(image: np.ndarray, transforms: Compose) -> np.ndarray:
    """Return augmented image (uint8 BGR)."""
    out = transforms(image=image)["image"]
    return out
