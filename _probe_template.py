"""探针：打印模板每个表格去重后每个单元格的完整文本，看清标签与空格关系"""
from docx import Document
from docx.oxml.ns import qn

doc = Document("/workspace/PQR模板.docx")

def cell_full_text(cell):
    return "\n".join(p.text for p in cell.paragraphs)

# 按物理 tc 元素去重
def unique_cells_in_row(row):
    seen = set()
    cells = []
    for cell in row.cells:
        tc_id = id(cell._tc)
        if tc_id not in seen:
            seen.add(tc_id)
            cells.append(cell)
    return cells

for ti, table in enumerate(doc.tables):
    print(f"\n{'='*70}")
    print(f"表格 {ti}  (rows={len(table.rows)})")
    print('='*70)
    for ri, row in enumerate(table.rows):
        cells = unique_cells_in_row(row)
        print(f"\n--- 行{ri} ({len(cells)}个独立单元格) ---")
        for ci, cell in enumerate(cells):
            txt = cell_full_text(cell).strip()
            # 获取 gridSpan
            gs = 1
            tcPr = cell._tc.find(qn('w:tcPr'))
            if tcPr is not None:
                gse = tcPr.find(qn('w:gridSpan'))
                if gse is not None:
                    gs = int(gse.get(qn('w:val')))
            label = txt.replace("\n", " ⏎ ") if txt else "〔空〕"
            print(f"  [{ri},{ci}] gs={gs}: {label[:80]}")
