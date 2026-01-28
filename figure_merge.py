from __future__ import annotations
from pathlib import Path
from PIL import Image

FIG_DIR = Path("/Volumes/T9/cfineProject/Figures")

paths = {
    "WCuff": FIG_DIR / "WCuff.png",
    "WoCuff": FIG_DIR / "WoCuff.png",
    "Area": FIG_DIR / "area_plot.png",
    "Eccentricity": FIG_DIR / "eccentricity_plot.png",
}

missing = [k for k, p in paths.items() if not p.exists()]
if missing:
    raise FileNotFoundError(f"Missing image(s): {missing}. Expected in: {FIG_DIR}")

OUT_PNG = FIG_DIR / "figure2x2.png"


def fit_to_cell(im: Image.Image, cell_w: int, cell_h: int, bg=(255, 255, 255)) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    scale = min(cell_w / w, cell_h / h)
    new_w = max(1, int(round(w * scale)))
    new_h = max(1, int(round(h * scale)))
    im_rs = im.resize((new_w, new_h), Image.Resampling.LANCZOS)

    cell = Image.new("RGB", (cell_w, cell_h), bg)
    x0 = (cell_w - new_w) // 2
    y0 = (cell_h - new_h) // 2
    cell.paste(im_rs, (x0, y0))
    return cell


imgs = {k: Image.open(p) for k, p in paths.items()}

cell_w = 1500
cell_h = 850

A = fit_to_cell(imgs["WCuff"], cell_w, cell_h)
B = fit_to_cell(imgs["WoCuff"], cell_w, cell_h)
C = fit_to_cell(imgs["Area"], cell_w, cell_h)
D = fit_to_cell(imgs["Eccentricity"], cell_w, cell_h)

gutter_x = 40
gutter_y = 40
margin = 30

out_w = margin * 2 + cell_w * 2 + gutter_x
out_h = margin * 2 + cell_h * 2 + gutter_y

canvas = Image.new("RGB", (out_w, out_h), (255, 255, 255))

x1 = margin
x2 = margin + cell_w + gutter_x
y1 = margin
y2 = margin + cell_h + gutter_y

canvas.paste(A, (x1, y1))
canvas.paste(B, (x2, y1))
canvas.paste(C, (x1, y2))
canvas.paste(D, (x2, y2))

canvas.save(OUT_PNG)
print(f"Saved: {OUT_PNG}")
