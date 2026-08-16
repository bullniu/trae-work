"""
解析 PQR模板.doc（OLE 复合二进制 Word 97-2003 格式）
步骤：
  1) olefile 解析容器结构
  2) 提取 WordDocument 流 - FIB - 定位 clx (piece table) - 提取文字
  3) 提取 1Table / 0Table 里的表格结构（grpprl）
  4) 按段落和表格边界输出结构化 JSON
"""
import olefile, struct, json, os, sys

FILE = "/workspace/PQR模板.doc"

def read_ole_stream(ole, stream_path):
    try:
        return ole.openstream(stream_path).read()
    except Exception as e:
        return None

def parse_piece_table(ole):
    """从 WordDocument 流 + 1Table/0Table 提取 piece table，返回完整文本 + 每段/每格边界"""
    word = read_ole_stream(ole, "WordDocument")
    if not word:
        return None
    # FIB at offset 0.  fcMin: 0x18 (4 bytes),  fcMac: 0x1C (4 bytes)
    #  fWhichTblStm: at 0xA bytes, bit 9 (0x200) = 1 means 1Table, else 0Table
    fcMin = struct.unpack_from("<I", word, 0x18)[0]
    fcMac = struct.unpack_from("<I", word, 0x1C)[0]
    flags1 = struct.unpack_from("<H", word, 0x0A)[0]
    tbl_name = "1Table" if (flags1 & 0x0200) else "0Table"
    tbl = read_ole_stream(ole, tbl_name)
    if not tbl:
        return None

    # FIB 里 fcClx / lcbClx 位置：
    #   https://learn.microsoft.com/en-us/openspecs/office_file_formats/ms-doc/a1b32832-e590-4659-88a5-7559bb4a4c40
    #   base offset of fcClx in FIB: 0x01A2 (4 bytes) fcClx; 0x01A6 (4 bytes) lcbClx
    #   but: for Word 97 it's at fcClx offset within fib base
    # Simpler: use the "clx" search in Table stream: scan for Prc entries ending with piece table
    # 实际上我们使用 fibRgLw97 / fcClx 字段：FIB base 的偏移：
    #   https://github.com/secureworks/oletools/blob/master/olefile/common.py
    #   fcClx at 0x1A2, lcbClx at 0x1A6
    try:
        fcClx  = struct.unpack_from("<I", word, 0x01A2)[0]
        lcbClx = struct.unpack_from("<I", word, 0x01A6)[0]
    except:
        return None
    clx = tbl[fcClx: fcClx + lcbClx]
    # clx 结构：可选 Prc (0x01 + cbGrpprl + grpprl) + 强制 Pcdt (0x02 + lcbPlcfpcd + Plcfpcd)
    pos = 0
    while pos < len(clx):
        t = clx[pos]
        if t == 0x01:
            # Prc
            pos += 1
            if pos + 2 > len(clx): break
            cb = struct.unpack_from("<H", clx, pos)[0]
            pos += 2 + cb
        elif t == 0x02:
            # Pcdt
            pos += 1
            if pos + 4 > len(clx): break
            lcbPlcfpcd = struct.unpack_from("<I", clx, pos)[0]
            pos += 4
            plcfpcd = clx[pos: pos + lcbPlcfpcd]
            # Plcfpcd: n+1 CPs (4 bytes each) then n PCDs (8 bytes each)
            cnt_piece = (len(plcfpcd) // 12) - 1  # (n+1)*4 + n*8 = 12n+4 => n = (L-4)/12
            total_cps = (cnt_piece + 1) * 4
            cps = struct.unpack_from("<" + "I" * (cnt_piece + 1), plcfpcd, 0)
            pcd_start = (cnt_piece + 1) * 4
            pieces_text = []
            for i in range(cnt_piece):
                pcd_bytes = plcfpcd[pcd_start + i*8 : pcd_start + (i+1)*8]
                fc_field = struct.unpack_from("<I", pcd_bytes, 2)[0]
                cp_start = cps[i]
                cp_end   = cps[i+1]
                char_count = cp_end - cp_start
                # bit 30 = fCompressed (ANSI) -> fc*2 offset, but each char is 1 byte
                if fc_field & 0x40000000:
                    # compressed: actual fc = (fc_field & ~0x40000000)>>1 ; each char is 1 byte
                    fc = (fc_field & 0xBFFFFFFF) >> 1
                    data = word[fc : fc + char_count]
                    try:
                        s = data.decode("cp1252", errors="replace")
                    except:
                        s = data.decode("latin-1", errors="replace")
                else:
                    # Unicode (UTF-16LE): char_count is # of chars, each 2 bytes
                    fc = fc_field & 0x3FFFFFFF
                    byte_cnt = char_count * 2
                    data = word[fc : fc + byte_cnt]
                    s = data.decode("utf-16-le", errors="replace")
                pieces_text.append(s)
            return "".join(pieces_text)
        else:
            # 未知，跳过
            break
    return None

def ole_list_streams(ole):
    return ole.listdir()

def dump_stream_sizes(ole):
    out = {}
    for path in ole.listdir():
        key = "/".join(path)
        try:
            data = ole.openstream(path).read()
            out[key] = len(data)
        except:
            pass
    return out

ole = olefile.OleFileIO(FILE)
print("=== OLE 根条目 ===")
for e in ole.listdir():
    print("  ", "/".join(e))

# Dump stream sizes
sizes = dump_stream_sizes(ole)
print("\n=== 流大小（Top 20）===")
for k, v in sorted(sizes.items(), key=lambda x: -x[1])[:20]:
    print(f"  {v:>9d} bytes  {k}")

# Extract text via piece table
text = parse_piece_table(ole)
if not text:
    # Fallback: brute-force decode UTF-16LE from WordDocument stream
    wd = read_ole_stream(ole, "WordDocument")
    # Extract printable ranges
    text = wd.decode("utf-16-le", errors="ignore")

# 清理控制字符但保留 换行/制表/段落标记
clean = []
for ch in text:
    code = ord(ch)
    if code in (0x000D, 0x000A, 0x000B, 0x000C, 0x0009):
        clean.append(ch)
    elif code < 0x0020:
        # Word 特殊标记符：段落 mark/换行/cell/行结束 保留成 \t|\n
        # 0x07 = cell end, 0x08 = ?, 13 = para end, 7 = cell end in table rows
        if code == 0x07:
            clean.append(" | ")   # cell boundary
        elif code == 0x08:
            clean.append("")
        else:
            clean.append("")
    elif code >= 0xF000:
        # private: keep?
        clean.append("")
    else:
        clean.append(ch)
clean_text = "".join(clean)

# 去掉重复空行保留结构
lines = clean_text.split("\n")
norm = []
for l in lines:
    l = l.replace("\r", "").strip()
    norm.append(l)
final = "\n".join(norm)

out_file = "/workspace/pqr_template_parsed.txt"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(final)
print(f"\n=== 解析文本已保存: {out_file} ({os.path.getsize(out_file)} bytes) ===")
print("=== 前5000字符预览 ===")
print(final[:5000])
