import pandas as pd
from .config import (
    RAW_TABLE_XLSX,
    AREA_BAR_SUMMARY_CSV,
    ECC_BAR_SUMMARY_CSV,
    AREA_PLOT_PNG,
    ECC_PLOT_PNG,
    UM_PER_PX
)
from .data_loader import load_raw_table
from .processing import (
    compute_group_stats, 
    compute_size_contrasts, 
    summarize_for_bars
)
from .plotting import plot_grouped_bars

def main():
    print("Starting analysis...")
    
    # 1. Load data
    df_raw = load_raw_table()
    
    # 2. Compute statistics
    df_group = compute_group_stats(df_raw)
    df_contrasts = compute_size_contrasts(df_raw)

    # 3. Save Tables
    # One Excel file, multiple sheets (clean)
    with pd.ExcelWriter(RAW_TABLE_XLSX, engine="openpyxl") as writer:
        df_raw.to_excel(writer, sheet_name="raw", index=False)
        df_group.to_excel(writer, sheet_name="group_stats", index=False)
        df_contrasts.to_excel(writer, sheet_name="contrasts", index=False)
    
    # 4. Process Summaries for Plotting
    summary_area = summarize_for_bars(df_raw, "area")
    summary_area.to_csv(AREA_BAR_SUMMARY_CSV, index=False)

    summary_ecc = summarize_for_bars(df_raw, "eccentricity")
    summary_ecc.to_csv(ECC_BAR_SUMMARY_CSV, index=False)

    # 5. Generate Plots
    units = "" if UM_PER_PX is None else " (µm²)"
    plot_grouped_bars(summary_area, y_label=f"Area{units}", title="Fascicle Area", save_path=AREA_PLOT_PNG)
    plot_grouped_bars(summary_ecc, y_label="Eccentricity", title="Fascicle Eccentricity", save_path=ECC_PLOT_PNG)

    print(f"Saved Excel (multi-sheet): {RAW_TABLE_XLSX}")
    print(f"Saved area bar summary: {AREA_BAR_SUMMARY_CSV}")
    print(f"Saved eccentricity bar summary: {ECC_BAR_SUMMARY_CSV}")
    print(f"Saved area plot: {AREA_PLOT_PNG}")
    print(f"Saved eccentricity plot: {ECC_PLOT_PNG}")

if __name__ == "__main__":
    main()
