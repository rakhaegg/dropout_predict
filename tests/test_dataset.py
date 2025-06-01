from pathlib import Path
from collections import Counter

def test_split_ratio():
    root = Path("data/processed")
    total = sum(1 for _ in root.rglob("*.[jp][pn]g"))
    train = sum(1 for _ in (root/"train").rglob("*.[jp][pn]g"))
    val   = sum(1 for _ in (root/"val").rglob("*.[jp][pn]g"))
    test  = sum(1 for _ in (root/"test").rglob("*.[jp][pn]g"))
    assert abs(train/total - 0.8) < 0.03
    assert abs(val/total   - 0.1) < 0.02
    assert abs(test/total  - 0.1) < 0.02

def test_class_balance():
    """ setiap label muncul di tiga split """
    root = Path("data/processed")
    splits = ["train", "val", "test"]
    labels = {p.name for p in (root/"train").iterdir() if p.is_dir()}
    for s in splits:
        assert labels == {p.name for p in (root/s).iterdir()}
