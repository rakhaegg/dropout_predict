import json, pathlib, functools

_PRICES_PATH = pathlib.Path(__file__).resolve().parent.parent / "prices.json"

@functools.lru_cache(maxsize=1)
def get_price(label: str) -> int | None:
    """Kembalikan harga IDR untuk label; None jika tidak ada."""
    with _PRICES_PATH.open() as f:
        data = json.load(f)
    return data.get(label)
