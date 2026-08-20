# -*- coding: utf-8 -*-
"""Dump raw tables from key pages so we can understand column structure."""
import pdfplumber
import json

INSPECT = [
    # (path, list of page indices (0-based) to dump)
    ("/workspace/GBT 14976-2025.pdf", [9, 10, 11, 12, 13, 14, 15]),  # 表1(热处理/密度) P10-16
    ("/workspace/GBT 9948-2025.pdf", [10, 11, 12, 13, 14, 15, 16]),   # 表1 热处理 P11, 表2? P12-14, 表3 P15, 表4 P16-17
    ("/workspace/GBT 36037-2018.pdf", [6, 7, 8, 9]),                  # 表1 焊剂类型 P7-8, 冶金性能 P9-10
    ("/workspace/NBT 47018.4-2022.pdf", [5, 6, 7, 10]),              # 表1 P6-7, 表2 P8, 附录A P11
]

for path, pages in INSPECT:
    print("=" * 90)
    print(f"FILE: {path}")
    with pdfplumber.open(path) as pdf:
        for pi in pages:
            if pi >= len(pdf.pages):
                continue
            page = pdf.pages[pi]
            text = (page.extract_text() or "")[:150].replace("\n", " | ")
            tables = page.extract_tables() or []
            print(f"\n----- P{pi+1} (tables={len(tables)}) TEXT: {text}")
            for ti, t in enumerate(tables):
                print(f"  TABLE[{ti}] rows={len(t)} cols={max((len(r) for r in t), default=0)}")
                for ri, row in enumerate(t[:6]):
                    # show row compactly
                    cells = [str(c).replace('\n',' ') if c is not None else '' for c in row]
                    print(f"    r{ri}: {cells}")
                if len(t) > 6:
                    print(f"    ... ({len(t)-6} more rows)")
                    for ri, row in enumerate(t[-3:]):
                        cells = [str(c).replace('\n',' ') if c is not None else '' for c in row]
                        print(f"    r{len(t)-3+ri}: {cells}")
