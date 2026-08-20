# -*- coding: utf-8 -*-
"""Debug: save cell crops, OCR full-row strips, verify coordinate alignment."""
import pdfplumber
import pymupdf
import pytesseract
from PIL import Image, ImageOps, ImageDraw
import io

path, idx = "/workspace/GBT 9948-2025.pdf", 11
dpi=450
doc = pymupdf.open(path)
pix = doc[idx].get_pixmap(matrix=pymupdf.Matrix(dpi/72, dpi/72))
img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
img_ac = ImageOps.autocontrast(img)
doc.close()
sx = dpi/72.0
print("image size:", img.size, "sx:", sx)

with pdfplumber.open(path) as pdf:
    page = pdf.pages[idx]
    edges = page.edges
    vxs = sorted(set(round(e["x0"]) for e in edges if abs(e["x0"]-e["x1"])<1))
    hys = sorted(set(round(e["top"]) for e in edges if abs(e["top"]-e["bottom"])<1))
    print("vxs:", vxs)
    print("hys:", hys)

# Draw grid lines on a copy to verify
dbg = img_ac.convert("RGB")
dr = ImageDraw.Draw(dbg)
for x in vxs:
    dr.line([(int(x*sx),0),(int(x*sx),dbg.height)], fill="red", width=2)
for y in hys:
    dr.line([(0,int(y*sx)),(dbg.width,int(y*sx))], fill="blue", width=2)
dbg.crop((0,0,dbg.width, min(dbg.height, int(330*sx)))).save("/workspace/_dbg_grid_top.png")
print("saved /workspace/_dbg_grid_top.png")

# OCR full row strip for row 5 (data) - hys[5] to hys[6]
y0, y1 = hys[5], hys[6]
strip = img_ac.crop((int(vxs[0]*sx), int(y0*sx), int(vxs[-1]*sx), int(y1*sx)))
strip = strip.resize((strip.width*2, strip.height*2), Image.LANCZOS)
strip.save("/workspace/_dbg_row5.png")
print("row5 strip size:", strip.size)
print("row5 OCR psm6:", repr(pytesseract.image_to_string(strip, lang="chi_sim+eng", config="--psm 6")))
print("row5 OCR psm7:", repr(pytesseract.image_to_string(strip, lang="chi_sim+eng", config="--psm 7")))

# OCR single cell row5 col3
x0,x1 = vxs[3], vxs[4]
cell = img_ac.crop((int(x0*sx), int(y0*sx), int(x1*sx), int(y1*sx)))
cell = cell.resize((cell.width*3, cell.height*3), Image.LANCZOS)
cell.save("/workspace/_dbg_cell_r5c3.png")
print("cell r5c3 size:", cell.size, "OCR psm7:", repr(pytesseract.image_to_string(cell, lang="chi_sim+eng", config="--psm 7")))
print("cell r5c3 OCR psm8:", repr(pytesseract.image_to_string(cell, lang="chi_sim+eng", config="--psm 8")))
print("cell r5c3 OCR psm10:", repr(pytesseract.image_to_string(cell, lang="chi_sim+eng", config="--psm 10")))

# Also OCR a strip covering rows 0-4 (header) to see what's there
hdr = img_ac.crop((int(vxs[0]*sx), int(hys[0]*sx), int(vxs[-1]*sx), int(hys[4]*sx)))
hdr.save("/workspace/_dbg_header.png")
print("header OCR psm6:", repr(pytesseract.image_to_string(hdr, lang="chi_sim+eng", config="--psm 6")[:400]))
