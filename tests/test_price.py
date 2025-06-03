from pathlib import Path
import sys


sys.path.append(str(Path(__file__).resolve().parents[1]))
from fruitscan.price import get_price

def test_known_label():
    assert get_price("apple") == 12000

def test_unknown_label():
    assert get_price("nonexistent") is None
