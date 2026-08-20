# -*- coding: utf-8 -*-
"""Dump OCR text for the scanned/OCR-based PDFs' key pages so we can fix parsers."""
import pymupdf, pytesseract
from PIL import Image, ImageOps
import io

def ocr(path, idx, dpi=400, psm=6):
    doc=pymupdf.open(path); pix=doc[idx].get_pixmap(matrix=pymupdf.Matrix(dpi/72,dpi/72))
    img=Image.open(io.BytesIO(pix.tobytes("png"))).convert("L"); doc.close()
    img=ImageOps.autocontrast(img)
    return pytesseract.image_to_string(img, lang="chi_sim+eng", config=f"--psm {psm}")

pages = [
    ("/workspace/GBT 36037-2018.pdf", 6, "36037 P7 焊剂表1"),
    ("/workspace/GBT 36037-2018.pdf", 7, "36037 P8 焊剂表1续"),
    ("/workspace/GBT 17854-2018.pdf", 5, "17854 P6 表1"),
    ("/workspace/GBT 39279-2020.pdf", 9, "39279 P10 表4力学"),
    ("/workspace/NBT 47018.4-2022.pdf", 5, "NBT P6 表1"),
    ("/workspace/NBT 47018.4-2022.pdf", 6, "NBT P7 表1续"),
    ("/workspace/NBT 47018.4-2022.pdf", 7, "NBT P8 表2力学"),
]
for path,idx,label in pages:
    print("="*80); print(f"### {label}")
    print(ocr(path,idx,400,6)[:1600])
