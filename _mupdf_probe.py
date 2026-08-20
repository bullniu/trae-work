"""用PyMuPDF测试乱码字体PDF的提取效果"""
import fitz

pdfs = [
    '/workspace/GBT 713.2-2023.pdf',
    '/workspace/GBT 5310-2023.pdf',
    '/workspace/GBT 5293-2018.pdf',
    '/workspace/GBT 5117-2012.pdf',
    '/workspace/GBT 36034-2018.pdf',
    '/workspace/GBT 9711-2017.pdf',
]

for p in pdfs:
    try:
        doc = fitz.open(p)
        print(f"\n=== {p.split('/')[-1]} ({doc.page_count}页) ===")
        for pi in [0, 1, 2]:
            if pi < doc.page_count:
                page = doc[pi]
                t = page.get_text()
                print(f"页{pi+1} ({len(t)}字符): {t[:150]}")
        doc.close()
    except Exception as e:
        print(f"{p}: ERR {e}")
