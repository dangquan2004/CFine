import pandas as pd
from .config import ROOT, SIZES_ORDER, CONDS_ORDER
from .utils import find_mask, metrics_from_binary_mask

def load_raw_table() -> pd.DataFrame:
    rows = []
    for n_dir in sorted(ROOT.glob("n=*")):
        if not n_dir.is_dir():
            continue

        for size in SIZES_ORDER:
            size_dir = n_dir / size
            if not size_dir.exists():
                continue

            paths = {c: find_mask(size_dir, c) for c in CONDS_ORDER}
            missing = [c for c, p in paths.items() if p is None]
            if missing:
                print(f"[SKIP] Missing {missing} in {size_dir}")
                continue

            for cond, p in paths.items():
                area, ecc = metrics_from_binary_mask(p)
                rows.append(
                    {
                        "n": n_dir.name,
                        "size": size,
                        "cond": cond,
                        "area": area,
                        "eccentricity": ecc,
                    }
                )

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No usable data found. Check ROOT path + folder/file naming.")
    return df
