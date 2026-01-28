from pathlib import Path

ROOT = Path("/Volumes/T9/cfineProject")

SIZES_ORDER = ["small", "medium"]
CONDS_ORDER = ["proximal", "cuff", "distal"]
LABEL_MAP = {"proximal": "Proximal", "cuff": "Cuff", "distal": "Distal"}

SIZE_LABELS = {
    "small": "12.8 × 7.0 mm",
    "medium": "12.8 × 9.8 mm",
}

UM_PER_PX: float | None = 11.4

TABLES_DIR = ROOT / "Tables"
FIGURES_DIR = ROOT / "Figures"
TABLES_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Single Excel output with multiple sheets
RAW_TABLE_XLSX = TABLES_DIR / "raw_table_area_eccentricity.xlsx"

# Keep your existing outputs
AREA_BAR_SUMMARY_CSV = TABLES_DIR / "area_bar_summary.csv"
ECC_BAR_SUMMARY_CSV = TABLES_DIR / "eccentricity_bar_summary.csv"
AREA_PLOT_PNG = FIGURES_DIR / "area_plot.png"
ECC_PLOT_PNG = FIGURES_DIR / "eccentricity_plot.png"
