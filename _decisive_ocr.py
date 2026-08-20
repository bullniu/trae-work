# -*- coding: utf-8 -*-
"""Decisive test: 600dpi eng-only on row strips + cells of garbled composition pages."""
import pdfplumber, pymupdf, pytesseract, re
from PIL import Image, ImageOps
import io

def render(path, idx, dpi=600):
    doc=pymupdf.open(path); pix=doc[idx].get_pixmap(matrix=pymupdf.Matrix(dpi/72,dpi/72))
    img=Image.open(io.BytesIO(pix.tobytes("png"))).convert("L"); doc.close()
    return ImageOps.autocontrast(img), dpi

for path, idx, label in [("/workspace/GBT 9948-2025.pdf",11,"9948 P12"),
                         ("/workspace/GBT 14976-2025.pdf",10,"14976 P11")]:
    print("="*80); print(label)
    img,dpi=render(path,idx,600); sx=dpi/72.0
    with pdfplumber.open(path) as pdf:
        page=pdf.pages[idx]
        vxs=sorted(set(round(e["x0"]) for e in page.edges if abs(e["x0"]-e["x1"])<1))
        hys=sorted(set(round(e["top"]) for e in page.edges if abs(e["top"]-e["bottom"])<1))
    # OCR a middle data row (row index 8) full strip, eng-only
    for ri in [6,8,10]:
        if ri>=len(hys)-1: continue
        y0,y1=hys[ri],hys[ri+1]
        strip=img.crop((int(vxs[0]*sx),int(y0*sx),int(vxs[-1]*sx),int(y1*sx)))
        strip=strip.resize((strip.width*2,strip.height*2),Image.LANCZOS)
        t=pytesseract.image_to_string(strip,lang="eng",config="--psm 6 -c tessedit_char_whitelist=0123456789.~—- ")
        print(f" row{ri} strip eng: {t.strip()[:300]!r}")
    # OCR each cell of row 8 eng-only psm7
    ri=8; y0,y1=hys[ri],hys[ri+1]; cells=[]
    for ci in range(len(vxs)-1):
        x0,x1=vxs[ci],vxs[ci+1]
        c=img.crop((int(x0*sx),int(y0*sx),int(x1*sx),int(y1*sx)))
        c=c.resize((c.width*3,c.height*3),Image.LANCZOS)
        t=pytesseract.image_to_string(c,lang="eng",config="--psm 8 -c tessedit_char_whitelist=0123456789.~—- ").strip()
        cells.append(t)
    print(f" row8 cells eng: {cells}")
