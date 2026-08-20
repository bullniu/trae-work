# -*- coding: utf-8 -*-
"""OCR key table pages of scanned PDFs (17854, 39279) at high DPI to assess parseability."""
import pymupdf, pytesseract
from PIL import Image, ImageOps
import io

def ocr(path, idx, dpi=400, psm=6):
    doc=pymupdf.open(path); pix=doc[idx].get_pixmap(matrix=pymupdf.Matrix(dpi/72,dpi/72))
    img=Image.open(io.BytesIO(pix.tobytes("png"))).convert("L"); doc.close()
    img=ImageOps.autocontrast(img)
    return pytesseract.image_to_string(img, lang="chi_sim+eng", config=f"--psm {psm}")

pages = [
    ("/workspace/GBT 17854-2018.pdf", 5, "17854 P6 型号/表1"),
    ("/workspace/GBT 17854-2018.pdf", 6, "17854 P7 力学性能表2"),
    ("/workspace/GBT 17854-2018.pdf", 9, "17854 P10 附录A焊剂化学成分"),
    ("/workspace/GBT 17854-2018.pdf", 10,"17854 P11 附录A续"),
    ("/workspace/GBT 39279-2020.pdf", 5, "39279 P6 化学成分表3"),
    ("/workspace/GBT 39279-2020.pdf", 9, "39279 P10 力学性能表4"),
    ("/workspace/GBT 39279-2020.pdf", 10,"39279 P11 力学性能续"),
    ("/workspace/GBT 39279-2020.pdf", 15,"39279 P16 型号对照表C1"),
    ("/workspace/GBT 39279-2020.pdf", 16,"39279 P17 型号对照续"),
]
for path,idx,label in pages:
    print("="*90); print(f"### {label}")
    t=ocr(path,idx,400,6)
    print(t[:1800])
