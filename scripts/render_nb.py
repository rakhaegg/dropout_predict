#!/usr/bin/env python3
import argparse
import subprocess
import pathlib
import sys

def main():
    ap = argparse.ArgumentParser(description="Render Jupyter Notebook to HTML")
    ap.add_argument("--src", required=True,
                    help="Path ke file .ipynb, misalnya notebooks/eda_dataset.ipynb")
    ap.add_argument("--dst", required=True,
                    help="Path lengkap output HTML, misalnya docs/eda_dataset.html")
    args = ap.parse_args()

    src_path = pathlib.Path(args.src)
    dst_path = pathlib.Path(args.dst)

    # Pastikan file sumber ada
    if not src_path.exists():
        print(f"Notebook source not found: {src_path}", file=sys.stderr)
        sys.exit(1)

    # Buat folder output jika belum ada
    dst_dir = dst_path.parent
    dst_dir.mkdir(parents=True, exist_ok=True)

    # Ekstrak nama file HTML saja (basename)
    output_basename = dst_path.name  # misal "eda_dataset.html"
    # Tentukan output directory
    output_dir = str(dst_dir)        # misal "docs"

    # Panggil nbconvert
    cmd = [
        "jupyter", "nbconvert",
        "--to", "html",
        str(src_path),
        "--output", output_basename,
        "--output-dir", output_dir
    ]
    print("🛠️ Menjalankan:", " ".join(cmd))
    return_code = subprocess.call(cmd)
    if return_code != 0:
        print(f"nbconvert gagal dengan kode {return_code}", file=sys.stderr)
        sys.exit(return_code)

if __name__ == "__main__":
    main()
