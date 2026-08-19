"""用 Spire.Doc.Free 把 PQR模板.doc 转为 .docx，便于后续 python-docx 处理"""
from spire.doc import Document, FileFormat

src = "/workspace/PQR模板.doc"
dst = "/workspace/PQR模板.docx"

doc = Document()
doc.LoadFromFile(src)
doc.SaveToFile(dst, FileFormat.Docx)
doc.Close()
print(f"已转换: {dst}")

# 校验
import os
print(f"文件大小: {os.path.getsize(dst)} bytes")
