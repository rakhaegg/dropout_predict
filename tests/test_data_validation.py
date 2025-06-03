import json, subprocess, pathlib, pytest
from collections import Counter

DATA_RAW = pathlib.Path("data/raw")
DATA_PROC = pathlib.Path("data/processed")
LABELS = [ln.strip() for ln in open("labels.txt")]

def test_sanity_check_pass():
    """pakai script sanity_check.py & baca exit-code"""
    res = subprocess.run(
        ["python", "scripts/sanity_check.py",
         "--root", DATA_RAW, "--out", "docs/tmp_report.json"],
        capture_output=True, text=True
    )
    assert res.returncode == 0, res.stdout + res.stderr
    report = json.load(open("docs/tmp_report.json"))
    assert report["corrupt"] == 0
    assert report["duplicates"] == 0

def test_label_completeness():
    """semua label wajib ada di train/val/test"""
    for split in ["train", "val", "test"]:
        found = {p.name for p in (DATA_PROC/split).iterdir() if p.is_dir()}
        assert set(LABELS) == found, f"Missing in {split}: {set(LABELS)-found}"

def test_split_ratio():                       # toleransi 2 %
    counts = {s: sum(1 for _ in (DATA_PROC/s).rglob("*.[jp][pn]g"))
              for s in ["train","val","test"]}
    total = sum(counts.values())
    assert abs(counts["train"]/total - .8) < .03
    assert abs(counts["val"]/total   - .1) < .02
    assert abs(counts["test"]/total  - .1) < .02
