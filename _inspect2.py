# -*- coding: utf-8 -*-
"""Inspect 14976 P9 (表1 rows1-17) and 9948 P10 (表1 rows1-11) full tables."""
import pdfplumber

for path, idx, label in [
    ("/workspace/GBT 14976-2025.pdf", 8, "14976 P9 表1(rows1-17)"),
    ("/workspace/GBT 9948-2025.pdf", 9, "9948 P10 表1(rows1-11)"),
    ("/workspace/GBT 9948-2025.pdf", 10, "9948 P11 表1续(rows12-27)"),
]:
    print("="*80); print(label)
    with pdfplumber.open(path) as pdf:
        page=pdf.pages[idx]
        tables=page.extract_tables() or []
        print(f" tables={len(tables)}")
        for ti,t in enumerate(tables):
            print(f" T[{ti}] rows={len(t)} cols={max((len(r) for r in t),default=0)}")
            for ri,row in enumerate(t):
                cells=[str(c).replace('\n',' ') if c is not None else '' for c in row]
                print(f"   r{ri}: {cells}")
