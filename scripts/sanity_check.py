#!/usr/bin/env python
"""
sanity_check.py – validasi dataset buah & sayur.
Usage: python sanity_check.py --root data/raw --out docs/data_report.json
"""
import argparse, json, hashlib, imghdr, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

def file_hash(p: Path, block=65536):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(block), b""):
            h.update(chunk)
    return h.hexdigest()

def inspect_image(path: Path, min_size=(64, 64)):
    try:
        img = Image.open(path)
        img.verify()                    # cek korup
        w, h = img.size
        status = "ok"
        if w < min_size[0] or h < min_size[1]:
            status = "small"
    except Exception:
        status = "corrupt"
        w = h = 0
    return dict(
        file=str(path.relative_to(ROOT)),
        w=w, h=h,
        hash=file_hash(path) if status == "ok" else None,
        status=status,
        label=path.parent.name
    )

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    ROOT = Path(args.root)

    images = list(ROOT.rglob("*.jp*g")) + list(ROOT.rglob("*.png"))
    with ThreadPoolExecutor() as ex:
        meta = list(ex.map(inspect_image, images))

    # Analisis agregat
    corrupt = [m for m in meta if m["status"] == "corrupt"]
    small   = [m for m in meta if m["status"] == "small"]

    # Deteksi duplikat (hanya untuk laporan, tidak dianggap error)
    hashes = {}
    dups = []
    for m in meta:
        if m["hash"]:
            if m["hash"] in hashes:
                dups.append((hashes[m["hash"]], m["file"]))
            else:
                hashes[m["hash"]] = m["file"]

    report = dict(
        total=len(meta),
        corrupt=len(corrupt),
        small=len(small),
        duplicates=len(dups),       # jumlah pasangan duplikat
        dup_pairs=dups[:20],        # contoh pasang duplikat (maks 20)
        by_label={}
    )
    for m in meta:
        report["by_label"].setdefault(m["label"], 0)
        report["by_label"][m["label"]] += 1

    # Tulis laporan JSON
    Path(args.out).write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

    # Exit non-zero hanya bila ada gambar corrupt
    if report["corrupt"] > 0:
        sys.exit("Data sanity check failed due to corrupt images!")
    # Duplikat tidak menyebabkan exit non-zero
