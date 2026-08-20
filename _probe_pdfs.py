# -*- coding: utf-8 -*-
"""Probe PDF structure: find pages containing key keywords and report table counts."""
import pdfplumber
import sys
import json

PDFS = [
    "/workspace/GBT 14976-2025.pdf",
    "/workspace/GBT 9948-2025.pdf",
    "/workspace/GBT 36037-2018.pdf",
    "/workspace/GBT 17854-2018.pdf",
    "/workspace/GBT 39279-2020.pdf",
    "/workspace/NBT 47018.4-2022.pdf",
]

KEYWORDS = ["化学成分", "力学性能", "牌号", "型号", "统一数字", "抗拉强度", "屈服强度", "延伸率",
            "熔敷金属", "焊丝", "焊剂", "Cr", "Ni", "Mo", "化学"]

for path in PDFS:
    print("=" * 80)
    print(f"FILE: {path}")
    try:
        with pdfplumber.open(path) as pdf:
            print(f"  Total pages: {len(pdf.pages)}")
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                hits = [kw for kw in KEYWORDS if kw in text]
                tables = page.extract_tables() or []
                tcount = len(tables)
                if hits or tcount:
                    snippet = text.replace("\n", " | ")[:200]
                    print(f"  P{i+1}: hits={hits[:8]} tables={tcount} | {snippet}")
    except Exception as e:
        print(f"  ERROR: {e}")
