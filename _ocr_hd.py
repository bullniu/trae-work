# -*- coding: utf-8 -*-
"""Test high-DPI OCR with preprocessing on garbled composition pages + scan all scanned-PDF pages."""
import pymupdf
import pytesseract
from PIL import Image, ImageOps
import io

def render(path, page_idx, dpi=500):
    doc = pymupdf.open(path)
    pix = doc[page_idx].get_pixmap(matrix=pymupdf.Matrix(dpi/72, dpi/72))
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
    doc.close()
    # autocontrast + threshold
    img = ImageOps.autocontrast(img)
    img = img.point(lambda x: 0 if x < 150 else 255, '1')
    return img

def ocr_img(img, psm=6):
    return pytesseract.image_to_string(img, lang="chi_sim+eng", config=f"--psm {psm}")

print("="*90)
print("HIGH-DPI OCR ON GARBLED COMPOSITION PAGES")
for path, idx, label in [
    ("/workspace/GBT 14976-2025.pdf", 10, "14976 P11 表2化学成分"),
    ("/workspace/GBT 9948-2025.pdf", 11, "9948 P12 表2化学成分"),
]:
    print(f"\n##### {label} (500dpi, psm6) #####")
    img = render(path, idx, 500)
    t = ocr_img(img, 6)
    print(t[:2000])

print("\n"+"="*90)
print("SCAN ALL PAGES OF SCANNED PDFs")
for path in ["/workspace/GBT 17854-2018.pdf","/workspace/GBT 39279-2020.pdf"]:
    print(f"\n##### {path} #####")
    doc = pymupdf.open(path)
    n = len(doc)
    doc.close()
    for i in range(n):
        img = render(path, i, 300)
        t = pytesseract.image_to_string(img, lang="chi_sim+eng", config="--psm 6")
        kws = ["化学成分","力学性能","牌号","型号","熔敷","抗拉","屈服","焊丝","焊剂","统一数字"]
        hits = [k for k in kws if k in t]
        snippet = t.replace("\n"," | ")[:180]
        print(f"  P{i+1} len={len(t)} hits={hits[:8]} | {snippet}")
