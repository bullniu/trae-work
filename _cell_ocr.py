# -*- coding: utf-8 -*-
"""OCR per-cell by cropping to table cell bboxes. Test on garbled composition pages."""
import pdfplumber
import pymupdf
import pytesseract
from PIL import Image
import io

def render_hi(path, page_idx, dpi=400):
    doc = pymupdf.open(path)
    pix = doc[page_idx].get_pixmap(matrix=pymupdf.Matrix(dpi/72, dpi/72))
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
    doc.close()
    return img, dpi

def ocr_cell(img, dpi, bbox, pad=3):
    # bbox in PDF points (x0, top, x1, bottom); scale to pixels
    sx = dpi/72.0
    x0 = max(0, int(bbox[0]*sx)-pad)
    y0 = max(0, int(bbox[1]*sx)-pad)
    x1 = img.width if int(bbox[2]*sx)+pad > img.width else int(bbox[2]*sx)+pad
    y1 = img.height if int(bbox[3]*sx)+pad > img.height else int(bbox[3]*sx)+pad
    crop = img.crop((x0, y0, x1, y1))
    # upscale small cells
    w, h = crop.size
    if max(w, h) < 60:
        crop = crop.resize((w*3, h*3), Image.LANCZOS)
    txt = pytesseract.image_to_string(crop, lang="chi_sim+eng", config="--psm 7 -c tessedit_char_whitelist=0123456789.~≤≥-—CSiMnPorNbcDEFkhVgWAluwMO/ ")
    return txt.strip().replace("\n", " ")

for path, idx, label in [
    ("/workspace/GBT 9948-2025.pdf", 11, "9948 P12 表2化学成分"),
    ("/workspace/GBT 14976-2025.pdf", 10, "14976 P11 表2化学成分"),
]:
    print("="*90)
    print(f"### {label}")
    img, dpi = render_hi(path, idx, 400)
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[idx]
        tables = page.find_tables()
        print(f"  found {len(tables)} tables")
        for ti, t in enumerate(tables):
            print(f"  --- TABLE[{ti}] rows={len(t.rows)} cols={len(t.cells[0]) if t.cells else 0}")
            # print header (first 2 rows) and first 4 data rows, per-cell OCR
            nrows = len(t.rows)
            for ri in range(min(nrows, 8)):
                row_cells = []
                for ci in range(len(t.cells[ri]) if ri < len(t.rows) else 0):
                    cell = t.cells[ri][ci]
                    if cell is None:
                        row_cells.append("")
                        continue
                    # cell is (x0, top, x1, bottom); but pdfplumber Table.cells gives bbox tuples
                    txt = ocr_cell(img, dpi, cell)
                    row_cells.append(txt)
                print(f"    r{ri}: {row_cells}")
