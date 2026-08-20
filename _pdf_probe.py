"""探针：检查各PDF页数和文字可提取性"""
import pdfplumber, os, glob

pdfs = sorted(glob.glob('/workspace/*.pdf'))
for p in pdfs:
    try:
        with pdfplumber.open(p) as pdf:
            n = len(pdf.pages)
            # 第一页文字
            t = pdf.pages[0].extract_text() or ''
            t_sample = t[:80].replace('\n',' / ').strip()
            print(f"{os.path.basename(p)}: {n}页 | 首80字: {t_sample}")
    except Exception as e:
        print(f"{os.path.basename(p)}: ERR {e}")
