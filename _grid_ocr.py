# -*- coding: utf-8 -*-
"""Build grid from line positions; OCR each cell. Test on garbled composition pages."""
import pdfplumber
import pymupdf
import pytesseract
from PIL import Image, ImageOps
import io

def render_hi(path, page_idx, dpi=450):
    doc = pymupdf.open(path)
    pix = doc[page_idx].get_pixmap(matrix=pymupdf.Matrix(dpi/72, dpi/72))
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
    img = ImageOps.autocontrast(img)
    doc.close()
    return img, dpi

def get_grid(page, snap=3):
    edges = page.edges
    vxs = sorted(set(round(e["x0"]) for e in edges if abs(e["x0"]-e["x1"])<1))
    hys = sorted(set(round(e["top"]) for e in edges if abs(e["top"]-e["bottom"])<1))
    # snap cluster
    def cluster(xs, tol=snap):
        out=[]
        for x in xs:
            if out and abs(x-out[-1])<=tol:
                continue
            out.append(x)
        return out
    return cluster(vxs), cluster(hys)

def ocr_cell(img, dpi, x0, y0, x1, y1, pad=2, psm=7, whitelist=None):
    sx = dpi/72.0
    cx0 = max(0, int(x0*sx)-pad); cy0 = max(0, int(y0*sx)-pad)
    cx1 = min(img.width, int(x1*sx)+pad); cy1 = min(img.height, int(y1*sx)+pad)
    if cx1<=cx0 or cy1<=cy0: return ""
    crop = img.crop((cx0, cy0, cx1, cy1))
    w,h = crop.size
    if max(w,h) < 70:
        crop = crop.resize((w*3, h*3), Image.LANCZOS)
    cfg = f"--psm {psm}"
    if whitelist:
        cfg += f" -c tessedit_char_whitelist={whitelist}"
    return pytesseract.image_to_string(crop, lang="chi_sim+eng", config=cfg).strip().replace("\n"," ")

for path, idx, label in [
    ("/workspace/GBT 9948-2025.pdf", 11, "9948 P12 表2化学成分"),
]:
    print("="*90); print(f"### {label}")
    img, dpi = render_hi(path, idx, 450)
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[idx]
        vxs, hys = get_grid(page)
        print(f"  vlines={len(vxs)} hlines={len(hys)}")
        print(f"  vxs={vxs}")
        # OCR header rows (first 3 rows) and first 3 data rows
        for ri in range(min(len(hys)-1, 6)):
            row=[]
            for ci in range(len(vxs)-1):
                x0,y0,x1,y1 = vxs[ci], hys[ri], vxs[ci+1], hys[ri+1]
                # first 3 cols are 序号/代号/牌号 (alpha+chinese); rest are composition (numeric)
                wl = None
                if ci >= 3:
                    wl = "0123456789.~—-≤≥"
                t = ocr_cell(img, dpi, x0, y0, x1, y1, psm=7, whitelist=wl)
                row.append(t)
            print(f"  r{ri}: {row}")
