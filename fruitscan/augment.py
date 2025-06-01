# fruitscan/augment.py

import random
import numpy as np
import cv2
from typing import Callable, Dict, Any

# Import ReplayCompose
from albumentations import (
    ReplayCompose, OneOf, Blur, CLAHE,
    HorizontalFlip, VerticalFlip, RandomBrightnessContrast,
    Affine
)

AUG_SEED = 42   # seed global

def get_train_transforms(size: int = 128) -> Callable[[np.ndarray], Dict[str, Any]]:
    """
    Kembalikan fungsi augmentasi deterministik:
      1) Panggil ReplayCompose sekali untuk menghasilkan 'image' + 'replay' params.
      2) Simpan 'replay' ke closure, kemudian panggil kembali ReplayCompose.replay(...) 
         dengan params yang sama agar hasil identik.
    """

    # Siapkan pipeline ReplayCompose (tanpa melakukan 'seed' karena ReplayCompose akan random sendiri
    # tetapi kita atur seed Python & NumPy sebelum pembuatan object-nya di runtime pertama).
    # Perhatikan: kita tidak membuat Compose di luar _augment_fn agar seed benar-benar terpanggil ulang.
    transform: ReplayCompose = None
    replay_params: Dict[str, Any] = {}

    def _augment_fn(image: np.ndarray) -> Dict[str, Any]:
        nonlocal transform, replay_params

        # Reset semua sumber acak agar urutan transform sama setiap kali fungsi ini baru dipakai
        random.seed(AUG_SEED)
        np.random.seed(AUG_SEED)

        if transform is None:
            # 1) Buat ReplayCompose pada pemanggilan pertama 
            transform = ReplayCompose(
                [
                   Affine(
                        translate_percent=0.05,    # setara shift_limit
                        scale=(0.95, 1.05),        # setara scale_limit=0.05
                        rotate=(-15, 15),          # setara rotate_limit
                        shear=0,                   # shear=0 jika tak ingin shearing
                        border_mode=cv2.BORDER_REFLECT_101,
                        p=0.7
                    ),
                    OneOf([
                        Blur(blur_limit=3, p=0.3),
                        CLAHE(clip_limit=2, p=0.7),
                    ], p=0.3),
                    HorizontalFlip(p=0.5),
                    VerticalFlip(p=0.1),
                    RandomBrightnessContrast(0.2, 0.2, p=0.5),
                ],
                p=1.0,
                # ReplayCompose secara default akan mengisi field 'replay' di hasilnya
            )

            # Terapkan transform sekali → dapatkan hasil + replay_params
            out = transform(image=image)
            replay_params = out["replay"]
            return {"image": out["image"]}
        else:
            # 2) Pada pemanggilan selanjutnya, pakai param yang sama untuk replay
            out = ReplayCompose.replay(replay_params, image=image)
            # ReplayCompose.replay hanya mengembalikan dict yang sudah berisi 'image'
            return {"image": out["image"]}

    return _augment_fn


def get_val_transforms(size: int = 128) -> Callable[[np.ndarray], Dict[str, Any]]:
    """
    Untuk validasi kita tidak melakukan augment; cukup kembalikan image apa adanya
    (tapi tetap reset seed supaya interface-nya konsisten).
    """
    def _val_fn(image: np.ndarray) -> Dict[str, Any]:
        random.seed(AUG_SEED)
        np.random.seed(AUG_SEED)
        # Tidak ada transformasi—just return image
        return {"image": image}

    return _val_fn


def apply_aug(image: np.ndarray, transforms_fn: Callable[[np.ndarray], Dict[str, Any]]) -> np.ndarray:
    """
    Wrapper: panggil transforms_fn(image=...) dan kembalikan array uint8 BGR-nya.
    """
    out_dict = transforms_fn(image=image)
    return out_dict["image"]
