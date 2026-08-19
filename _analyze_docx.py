"""
分析 PQR模板.docx 的精确结构：
- 遍历每个 Section、Paragraph、Table
- 记录每个表格的行数、列数、每个单元格的内容（包括空单元格）
- 输出结构化 JSON，用于指导填充脚本定位"空格"位置
"""
from docx import Document
from docx.oxml.ns import qn
import json

doc = Document("/workspace/PQR模板.docx")

def cell_text(cell):
    """获取单元格所有段落文本，用 \\n 连接"""
    parts = []
    for p in cell.paragraphs:
        parts.append(p.text)
    return "\n".join(parts)

# 遍历 body 元素，保留段落与表格的顺序
body = doc.element.body
result = {"paragraphs": [], "tables": []}

def iter_block_items(parent):
    """按文档顺序遍历 block-level 元素（段落 <w:p> 或表格 <w:tbl>）"""
    for child in parent.iterchildren():
        if child.tag == qn('w:p'):
            yield ('p', child)
        elif child.tag == qn('w:tbl'):
            yield ('tbl', child)

from docx.text.paragraph import Paragraph
from docx.table import Table

seq = 0
for kind, el in iter_block_items(body):
    seq += 1
    if kind == 'p':
        p = Paragraph(el, doc)
        t = p.text.strip()
        if t:
            result["paragraphs"].append({"seq": seq, "text": t})
    elif kind == 'tbl':
        tbl = Table(el, doc)
        rows_info = []
        for ri, row in enumerate(tbl.rows):
            cells_info = []
            seen_cells = set()
            for ci, cell in enumerate(row.cells):
                # tc 元素唯一标识，避免重复（合并单元格会重复）
                tc_el = cell._tc
                tc_id = id(tc_el)
                if tc_id in seen_cells:
                    cells_info.append({"dup": True})
                    continue
                seen_cells.add(tc_id)
                # gridSpan / vMerge 信息
                grid_span = 1
                vmerge = False
                tcPr = tc_el.find(qn('w:tcPr'))
                if tcPr is not None:
                    gs = tcPr.find(qn('w:gridSpan'))
                    if gs is not None:
                        grid_span = int(gs.get(qn('w:val')))
                    vm = tcPr.find(qn('w:vMerge'))
                    if vm is not None:
                        vmerge = True
                        vm_val = vm.get(qn('w:val'))
                        vmerge = vm_val != 'restart' if vm_val else True
                cells_info.append({
                    "text": cell_text(cell).strip(),
                    "grid_span": grid_span,
                    "vmerge_cont": vmerge
                })
            rows_info.append({"row_idx": ri, "cells": cells_info})
        result["tables"].append({"seq": seq, "nrows": len(tbl.rows), "rows": rows_info})

with open("/workspace/pqr_template_struct.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"段落数（非空）: {len(result['paragraphs'])}")
print(f"表格数: {len(result['tables'])}")
print("\n=== 各表格概览 ===")
for t in result['tables']:
    print(f"\n表格 seq={t['seq']} 行数={t['nrows']}")
    for r in t['rows'][:3]:  # 只打印前3行预览
        cells_preview = []
        for c in r['cells']:
            if c.get('dup'):
                cells_preview.append('〈同左〉')
            elif c.get('vmerge_cont'):
                cells_preview.append('〈同上〉')
            else:
                txt = c['text'][:20].replace('\n','/') if c['text'] else '·空·'
                cells_preview.append(f"[{txt}]" + (f"×{c['grid_span']}" if c['grid_span']>1 else ''))
        print(f"  行{r['row_idx']}: {' | '.join(cells_preview)}")
print("\n结构已保存: /workspace/pqr_template_struct.json")
