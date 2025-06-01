import numpy as np, cv2, random, pytest
from fruitscan.augment import get_train_transforms, AUG_SEED

def test_deterministic():
    random.seed(AUG_SEED)
    img = np.ones((128,128,3), dtype=np.uint8)*127
    tf = get_train_transforms()
    out1 = tf(image=img)["image"]
    random.seed(AUG_SEED)
    tf = get_train_transforms()
    out2 = tf(image=img)["image"]
    assert np.array_equal(out1, out2), "Augmentation should be deterministic with same seed"

def test_shape_preserved():
    img = np.zeros((128,128,3), dtype=np.uint8)
    out = get_train_transforms()(image=img)["image"]
    assert out.shape == img.shape
