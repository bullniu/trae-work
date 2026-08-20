"""提取NBT 47014-2023关键内容：找附录C母材分类、附录D焊材分类、覆盖范围规则"""
import pdfplumber, re

PDF = '/workspace/NBT 47014-2023.pdf'

with pdfplumber.open(PDF) as pdf:
    # 先扫描全部页找"附录C""附录D""母材分类""焊材分类""覆盖范围"
    keywords = ['附录C', '附录D', '附录 c', '附录 d', '母材分类', '焊材分类',
                '类别号', '组别号', '覆盖范围', '厚度范围', '熔敷金属厚度']
    hits = {}
    for pi, page in enumerate(pdf.pages):
        t = page.extract_text() or ''
        for k in keywords:
            if k in t:
                hits.setdefault(k, []).append(pi+1)

    print("=== 关键词命中页码 ===")
    for k, pages in hits.items():
        print(f"{k}:  {pages[:30]}")
