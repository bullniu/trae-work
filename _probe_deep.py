# -*- coding: utf-8 -*-
"""Deep probe for PDFs that returned no hits/tables."""
import pdfplumber

PDFS = [
    "/workspace/GBT 17854-2018.pdf",
    "/workspace/GBT 39279-2020.pdf",
]

for path in PDFS:
    print("=" * 80)
    print(f"FILE: {path}")
    with pdfplumber.open(path) as pdf:
        print(f"  Total pages: {len(pdf.pages)}")
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            chars = len(text)
            # default tables
            tables_def = page.extract_tables() or []
            # try with explicit line/text settings
            tables_strict = page.extract_tables(table_settings={
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines",
            }) or []
            tables_text = page.extract_tables(table_settings={
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
            }) or []
            # find keywords
            kws = ["化学成分", "力学性能", "牌号", "型号", "焊丝", "焊剂", "Cr", "Ni", "Mo",
                   "抗拉", "屈服", "延伸", "熔敷", "统一数字"]
            hits = [kw for kw in kws if kw in text]
            snippet = text.replace("\n", " | ")[:300]
            print(f"  P{i+1}: chars={chars} hits={hits[:8]} t_def={len(tables_def)} t_strict={len(tables_strict)} t_text={len(tables_text)}")
            print(f"      TEXT: {snippet}")
