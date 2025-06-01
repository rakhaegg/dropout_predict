# tests/test_augment.py

from pathlib import Path
import random
import sys
import numpy as np
import cv2
import pytest
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fruitscan.augment import get_train_transforms, AUG_SEED

def test_deterministic():
    # Buat gambar input abu‐abu (128×128)
    img = np.ones((128, 128, 3), dtype=np.uint8) * 127

    # Dapatkan fungsi augmentasi baru
    tf = get_train_transforms()

    # Panggil pertama kali (bisa dianggap "generate replay_params")
    random.seed(AUG_SEED)
    img1 = tf(image=img)["image"]

    # Panggil kedua kali: simpan ulang seed agar closure meng-capture seed yang sama
    random.seed(AUG_SEED)
    img2 = tf(image=img)["image"]

    assert img1.shape == (128, 128, 3)
    assert img2.shape == (128, 128, 3)
    assert np.array_equal(img1, img2), "Augmentation harus deterministik dengan replay_params yang sama"


def test_shape_preserved():
    img = np.zeros((128, 128, 3), dtype=np.uint8)
    tf = get_train_transforms()

    transformed = tf(image=img)["image"]
    assert transformed.shape == img.shape
