#!/usr/bin/env python3
"""
split.py – stratified split fruit & veg dataset
"""
import argparse, shutil, random
from pathlib import Path
from collections import Counter
from sklearn.model_selection import train_test_split

SEED = 42
random.seed(SEED)

def list_images(root):
    return [p for p in root.rglob("*.*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"}]

def copy_files(files, dst_root):
    for src in files:
        dst = dst_root / src.parent.name / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="data/raw")
    ap.add_argument("--dst", default="data/processed")
    ap.add_argument("--train", type=float, default=0.8)
    ap.add_argument("--val", type=float, default=0.1)
    args = ap.parse_args()

    src_root = Path(args.src)
    dst_root = Path(args.dst)
    imgs = list_images(src_root)
    labels = [p.parent.name for p in imgs]

    train_files, temp_files, train_lbl, temp_lbl = train_test_split(
        imgs, labels, stratify=labels, test_size=(1 - args.train), random_state=SEED
    )
    val_ratio = args.val / (1 - args.train)
    val_files, test_files = train_test_split(
        temp_files, stratify=temp_lbl, test_size=1 - val_ratio, random_state=SEED
    )
    splits = {"train": train_files, "val": val_files, "test": test_files}

    # copy
    for split, files in splits.items():
        copy_files(files, dst_root / split)

    # simple report
    for split, files in splits.items():
        cnt = Counter(p.parent.name for p in files)
        total = sum(cnt.values())
        print(f"{split}: {total} images – {len(cnt)} classes")
