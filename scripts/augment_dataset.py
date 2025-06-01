#!/usr/bin/env python
"""
Generate N augmented samples per class for visual inspection.
"""
import argparse, random
import sys
from pathlib import Path
import cv2
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fruitscan.augment import get_train_transforms, AUG_SEED

def main(src_dir: str, dst_dir: str, n: int):
    random.seed(AUG_SEED)
    src_root = Path(src_dir)
    dst_root = Path(dst_dir)
    dst_root.mkdir(parents=True, exist_ok=True)
    tfm = get_train_transforms()

    for label_dir in src_root.iterdir():
        if not label_dir.is_dir():
            continue
        imgs = list(label_dir.glob("*"))
        random.shuffle(imgs)
        for i, img_path in enumerate(imgs[:n]):
            img = cv2.imread(str(img_path))
            aug = tfm(image=img)["image"]
            out_name = f"{label_dir.name}_{i}.jpg"
            cv2.imwrite(str(dst_root / out_name), aug)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="data/processed/train")
    ap.add_argument("--dst", default="docs/aug_samples")
    ap.add_argument("-n", "--num", type=int, default=3)
    args = ap.parse_args()
    main(args.src, args.dst, args.num)
