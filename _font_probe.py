# -*- coding: utf-8 -*-
"""Investigate fonts and raw glyph IDs on garbled pages to crack the cipher."""
import pymupdf

for path, idx in [("/workspace/GBT 14976-2025.pdf", 10), ("/workspace/GBT 9948-2025.pdf", 11)]:
    print("="*80)
    print(f"{path} P{idx+1}")
    doc = pymupdf.open(path)
    page = doc[idx]
    # fonts
    fonts = page.get_fonts(full=True)
    print("FONTS:", fonts[:5])
    # raw character info
    d = page.get_text("rawdict")
    # collect (glyph_id, text) pairs
    pairs = {}
    for blk in d.get("blocks", []):
        for line in blk.get("lines", []):
            for sp in line.get("spans", []):
                fname = sp.get("font","")
                for ch in sp.get("chars", []):
                    c = ch.get("c", "")
                    gid = ch.get("c", "")  # placeholder
                    # rawdict char has 'c' = unicode, 'bbox'; we want the origin char code
                    pairs.setdefault((fname, c), 0)
                    pairs[(fname, c)] += 1
    print("FONT/CHAR counts (top 40):")
    for k,v in sorted(pairs.items(), key=lambda x:-x[1])[:40]:
        print(f"   {k} -> {v}")
    doc.close()

# Try: extract using get_text trace / check xref fonts
print("="*80)
print("FONT XREF details for 14976 P11")
doc = pymupdf.open("/workspace/GBT 14976-2025.pdf")
page = doc[10]
for f in page.get_fonts(full=True):
    xref = f[0]
    print("Font xref", xref, "name", f[3], "type", f[2], "enc", f[5] if len(f)>5 else "?")
    try:
        doc.extract_font(xref)
        ext = doc.extract_font(xref)
        print("   extracted:", ext[0], len(ext[1]) if ext[1] else 0, "bytes", ext[2] if len(ext)>2 else "")
    except Exception as e:
        print("   extract err", e)
doc.close()
