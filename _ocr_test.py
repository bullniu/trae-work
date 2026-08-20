# -*- coding: utf-8 -*-
"""OCR test on garbled pages and scanned pages to verify approach & locate 表1 starts."""
import pymupdf
import pytesseract
from PIL import Image
import io

# Render page at 300 DPI -> OCR with chi_sim+eng
def ocr_page(path, page_idx, dpi=300):
    doc = pymupdf.open(path)
    page = doc[page_idx]
    mat = pymupdf.Matrix(dpi/72, dpi/72)
    pix = page.get_pixmap(matrix=mat)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    doc.close()
    txt = pytesseract.image_to_string(img, lang="chi_sim+eng", config="--psm 6")
    return txt

tests = [
    # verify garbled pages are composition tables
    ("/workspace/GBT 14976-2025.pdf", 10, "14976 P11 (garbled - expect 表2 化学成分?)"),
    ("/workspace/GBT 14976-2025.pdf", 8,  "14976 P9 (find 表1 start rows 1-17)"),
    ("/workspace/GBT 9948-2025.pdf", 9,   "9948 P10 (find 表1 start rows 1-11)"),
    ("/workspace/GBT 9948-2025.pdf", 11,  "9948 P12 (garbled - expect 表2 化学成分)"),
    # scanned pdfs
    ("/workspace/GBT 17854-2018.pdf", 0,  "17854 P1 (scanned cover)"),
    ("/workspace/GBT 17854-2018.pdf", 4,  "17854 P5 (scanned - expect content)"),
    ("/workspace/GBT 39279-2020.pdf", 0,  "39279 P1 (scanned cover)"),
    ("/workspace/GBT 39279-2020.pdf", 4,  "39279 P5 (scanned - expect content)"),
]

for path, idx, label in tests:
    print("=" * 90)
    print(f"TEST: {label}")
    try:
        txt = ocr_page(path, idx)
        print(f"[OCR len={len(txt)}]")
        print(txt[:1500])
    except Exception as e:
        print(f"ERROR: {e}")
