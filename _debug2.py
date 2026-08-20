# -*- coding: utf-8 -*-
"""Check pdfplumber text for 36037 P7-8 and NBT47018 P8; OCR 17854 P6 first column."""
import pdfplumber, pymupdf, pytesseract, re
from PIL import Image, ImageOps
import io

def ocr_img(img, psm=6, lang="chi_sim+eng", wl=None):
    cfg=f"--psm {psm}"
    if wl: cfg+=f" -c tessedit_char_whitelist={wl}"
    return pytesseract.image_to_string(img, lang=lang, config=cfg)

print("="*80); print("36037 P7-8 pdfplumber TEXT:")
with pdfplumber.open("/workspace/GBT 36037-2018.pdf") as pdf:
    for idx in (6,7):
        t = pdf.pages[idx].extract_text() or ""
        print(f"--- P{idx+1} ---")
        print(t[:900])

print("\n"+"="*80); print("NBT47018 P8 pdfplumber TEXT:")
with pdfplumber.open("/workspace/NBT 47018.4-2022.pdf") as pdf:
    t = pdf.pages[7].extract_text() or ""
    print(t[:1200])

print("\n"+"="*80); print("17854 P6 first-column OCR (型号 column):")
doc=pymupdf.open("/workspace/GBT 17854-2018.pdf")
pix=doc[5].get_pixmap(matrix=pymupdf.Matrix(600/72,600/72))
img=Image.open(io.BytesIO(pix.tobytes("png"))).convert("L"); doc.close()
img=ImageOps.autocontrast(img)
# page is ~595pt wide; table 型号 col approx x[55,150] pts -> at 600dpi *8.33
sx=600/72.0
crop=img.crop((int(50*sx), int(180*sx), int(160*sx), int(700*sx)))
crop=crop.resize((crop.width*2, crop.height*2), Image.LANCZOS)
print("psm6:", repr(ocr_img(crop,6)))
print("psm4:", repr(ocr_img(crop,4)))
# Try whole left half
crop2=img.crop((int(50*sx), int(180*sx), int(200*sx), int(720*sx)))
crop2=crop2.resize((crop2.width*2, crop2.height*2), Image.LANCZOS)
print("left-half psm6:", repr(ocr_img(crop2,6)[:1500]))
