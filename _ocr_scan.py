# -*- coding: utf-8 -*-
"""Test pymupdf text on garbled pages; OCR all pages of scanned PDFs to find tables."""
import pymupdf
import pytesseract
from PIL import Image
import io

def ocr_page(path, page_idx, dpi=300):
    doc = pymupdf.open(path)
    page = doc[page_idx]
    pix = page.get_pixmap(matrix=pymupdf.Matrix(dpi/72, dpi/72))
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    doc.close()
    return pytesseract.image_to_string(img, lang="chi_sim+eng", config="--psm 6")

print("="*90)
print("PYMUPDF TEXT ON GARBLED PAGES")
for path, idx in [("/workspace/GBT 14976-2025.pdf",10),("/workspace/GBT 14976-2025.pdf",11),
                  ("/workspace/GBT 9948-2025.pdf",11),("/workspace/GBT 9948-2025.pdf",12)]:
    doc = pymupdf.open(path)
    t = doc[idx].get_text()
    doc.close()
    print(f"\n--- {path} P{idx+1} pymupdf len={len(t)} ---")
    print(t[:600].replace("\n"," | "))

print("\n"+"="*90)
print("OCR ALL PAGES OF SCANNED PDFs (find table pages)")
for path in ["/workspace/GBT 17854-2018.pdf","/workspace/GBT 39279-2020.pdf"]:
    print(f"\n##### {path} #####")
    doc = pymupdf.open(path)
    for i in range(len(doc)):
        doc.close()
        t = ocr_page(path, i)
        kws = ["化学成分","力学性能","牌号","型号","熔敷","抗拉","屈服","焊丝","焊剂","统一数字","表"]
        hits = [k for k in kws if k in t]
        snippet = t.replace("\n"," | ")[:200]
        print(f"  P{i+1} len={len(t)} hits={hits[:8]} | {snippet}")
