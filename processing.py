import pandas as pd
from .config import SIZES_ORDER, CONDS_ORDER

def compute_group_stats(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    mean ± SD per (size, cond) for area and eccentricity.
    """
    out = (
        df_raw.groupby(["size", "cond"], as_index=False)
        .agg(
            n_obs=("area", lambda x: int(x.notna().sum())),
            area_mean=("area", "mean"),
            area_sd=("area", "std"),
            ecc_mean=("eccentricity", "mean"),
            ecc_sd=("eccentricity", "std"),
        )
    )
    out["size"] = pd.Categorical(out["size"], categories=SIZES_ORDER, ordered=True)
    out["cond"] = pd.Categorical(out["cond"], categories=CONDS_ORDER, ordered=True)
    return out.sort_values(["size", "cond"])


def compute_size_contrasts(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Your requested contrasts (2 rows: small, medium):
      - area: mean proximal, mean cuff, proximal - cuff
      - ecc:  mean cuff, mean proximal, cuff - proximal
    """
    rows = []
    for size in SIZES_ORDER:
        area_mean_prox = df_raw.loc[(df_raw["size"] == size) & (df_raw["cond"] == "proximal"), "area"].mean()
        area_mean_cuff = df_raw.loc[(df_raw["size"] == size) & (df_raw["cond"] == "cuff"), "area"].mean()
        area_diff_prox_minus_cuff = area_mean_prox - area_mean_cuff

        ecc_mean_cuff = df_raw.loc[(df_raw["size"] == size) & (df_raw["cond"] == "cuff"), "eccentricity"].mean()
        ecc_mean_prox = df_raw.loc[(df_raw["size"] == size) & (df_raw["cond"] == "proximal"), "eccentricity"].mean()
        ecc_diff_cuff_minus_prox = ecc_mean_cuff - ecc_mean_prox

        rows.append(
            {
                "size": size,
                "area_mean_proximal": area_mean_prox,
                "area_mean_cuff": area_mean_cuff,
                "area_diff_prox_minus_cuff": area_diff_prox_minus_cuff,
                "ecc_mean_cuff": ecc_mean_cuff,
                "ecc_mean_proximal": ecc_mean_prox,
                "ecc_diff_cuff_minus_prox": ecc_diff_cuff_minus_prox,
            }
        )

    out = pd.DataFrame(rows)
    out["size"] = pd.Categorical(out["size"], categories=SIZES_ORDER, ordered=True)
    return out.sort_values("size")


def summarize_for_bars(df_raw: pd.DataFrame, value_col: str) -> pd.DataFrame:
    out = (
        df_raw.groupby(["size", "cond"], as_index=False)
        .agg(
            mean=(value_col, "mean"),
            standard_deviation=(value_col, "std"),
            n=(value_col, lambda x: int(x.notna().sum())),
        )
    )
    out["size"] = pd.Categorical(out["size"], categories=SIZES_ORDER, ordered=True)
    out["cond"] = pd.Categorical(out["cond"], categories=CONDS_ORDER, ordered=True)
    return out.sort_values(["size", "cond"])
