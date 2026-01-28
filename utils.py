from pathlib import Path
import numpy as np
import tifffile as tiff
from skimage.measure import label, regionprops
from .config import UM_PER_PX

def find_mask(size_dir: Path, cond: str) -> Path | None:
    candidates = [size_dir / f"{cond}.tif", size_dir / "mask" / f"{cond}.tif"]
    for c in candidates:
        if c.exists():
            return c
    hits = list(size_dir.glob(f"**/{cond}.tif"))
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        print(f"[WARN] Multiple matches for {cond}.tif under {size_dir}; using first: {hits[0]}")
        return hits[0]
    return None


def _as_2d(arr: np.ndarray, path: Path) -> np.ndarray:
    if arr.ndim == 2:
        return arr
    if arr.ndim == 3 and 1 in arr.shape:
        arr2 = np.squeeze(arr)
        if arr2.ndim == 2:
            return arr2
    raise ValueError(f"{path} is not 2D (or singleton-3D). Got shape={arr.shape}")


def metrics_from_binary_mask(mask_path: Path) -> tuple[float, float]:
    arr = tiff.imread(mask_path)
    arr = _as_2d(arr, mask_path)

    fg = (arr == 1)

    area_px = float(fg.sum())
    area = area_px if UM_PER_PX is None else area_px * (UM_PER_PX ** 2)

    lab = label(fg)
    props = regionprops(lab)
    if len(props) == 0:
        ecc = np.nan
    else:
        areas = np.array([p.area for p in props], dtype=float)
        eccs = np.array([p.eccentricity for p in props], dtype=float)
        ecc = float(np.average(eccs, weights=areas))

    return area, ecc
