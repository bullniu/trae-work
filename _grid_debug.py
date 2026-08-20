# -*- coding: utf-8 -*-
"""Debug table grid: vertical/horizontal line positions for garbled composition pages."""
import pdfplumber

for path, idx, label in [
    ("/workspace/GBT 9948-2025.pdf", 11, "9948 P12"),
    ("/workspace/GBT 14976-2025.pdf", 10, "14976 P11"),
]:
    print("="*80)
    print(f"### {label}")
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[idx]
        print(f"  page size: {page.width} x {page.height}")
        # edges
        edges = page.edges
        # vertical edges (x constant-ish), horizontal edges (y constant-ish)
        vxs = sorted(set(round(e["x0"]) for e in edges if abs(e["x0"]-e["x1"])<1))
        hys = sorted(set(round(e["top"]) for e in edges if abs(e["top"]-e["bottom"])<1))
        print(f"  #vertical line x-positions: {len(vxs)}: {vxs}")
        print(f"  #horizontal line y-positions: {len(hys)}: {hys}")
        # find_tables with explicit lines strategy
        ts = {"vertical_strategy":"lines","horizontal_strategy":"lines",
              "snap_tolerance": 3, "join_tolerance": 3}
        tables = page.find_tables(table_settings=ts)
        print(f"  find_tables(lines): {len(tables)} tables")
        for ti,t in enumerate(tables):
            print(f"    T[{ti}] bbox={t.bbox} rows={len(t.rows)} cols={len(t.cells[0]) if t.cells else 0}")
            # show first row cell bboxes
            if t.cells:
                row0 = t.cells[0]
                print(f"    row0 cells x0s: {[round(c[0],1) if c else None for c in row0]}")
        # also try text strategy
        ts2 = {"vertical_strategy":"text","horizontal_strategy":"text","snap_tolerance":3}
        tables2 = page.find_tables(table_settings=ts2)
        print(f"  find_tables(text): {len(tables2)} tables")
        for ti,t in enumerate(tables2[:1]):
            print(f"    T[{ti}] rows={len(t.rows)} cols={len(t.cells[0]) if t.cells else 0}")
