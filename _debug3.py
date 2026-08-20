# -*- coding: utf-8 -*-
import pdfplumber, pymupdf, pytesseract, re
from PIL import Image, ImageOps
import io

def ocr(path, idx, dpi=450):
    doc=pymupdf.open(path); pix=doc[idx].get_pixmap(matrix=pymupdf.Matrix(dpi/72,dpi/72))
    img=Image.open(io.BytesIO(pix.tobytes("png"))).convert("L"); doc.close()
    return pytesseract.image_to_string(ImageOps.autocontrast(img), lang="chi_sim+eng", config="--psm 6")

print("="*70); print("NBT47018 P6-7 table cells (raw):")
with pdfplumber.open("/workspace/NBT 47018.4-2022.pdf") as pdf:
    for idx in (5,6):
        for ti,t in enumerate(pdf.pages[idx].extract_tables() or []):
            print(f" P{idx+1} T[{ti}] rows={len(t)}")
            for row in t[:18]:
                cells=[ (c.replace('\n',' ') if c else '') for c in row]
                print("   ", cells)

print("\n"+"="*70); print("39279 normalized model matches:")
txt = ocr("/workspace/GBT 39279-2020.pdf",9)+"\n"+ocr("/workspace/GBT 39279-2020.pdf",10)+"\n"+ocr("/workspace/GBT 39279-2020.pdf",15)+"\n"+ocr("/workspace/GBT 39279-2020.pdf",16)
norm = re.sub(r"(?i)x","X", txt)
norm = re.sub(r"(49|55|62)\s+X\s*", r"\1X", norm)
norm = re.sub(r"(49|55|62)X\s+", r"\1X", norm)
ms = re.findall(r"\b(49|55|62)X(\d{0,2}[A-Za-z][A-Za-z0-9]{0,8})\b", norm)
print("matches:", sorted(set("G"+a+"X"+b.upper() for a,b in ms)))
# show lines containing 49/55/62
print("--- lines w/ strength ---")
for line in txt.split("\n"):
    if re.search(r"\b(49|55|62)\b", line):
        print("  ", line.strip()[:120])
