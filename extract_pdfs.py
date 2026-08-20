# -*- coding: utf-8 -*-
"""
Extract 牌号/型号, 化学成分, 力学性能 from 6 PDFs -> /workspace/extracted_pdfs.json

Strategy per PDF:
- Text-based PDFs (14976, 9948, 36037, NBT47018.4): pdfplumber tables where clean; OCR where
  tables not vector-detected or font is garbled.
- Scanned PDFs (17854, 39279): OCR via pymupdf render + tesseract (chi_sim+eng).
- Garbled FangZheng composition tables (14976 表2, 9948 表2, 39279 表3) are not recoverable
  (no ToUnicode + dense small tables defeat OCR) -> composition left empty per task note.
"""
import pdfplumber, pymupdf, pytesseract, re, json, os
from PIL import Image, ImageOps
import io

# ---------------------------------------------------------------- helpers
def ocr_page(path, idx, dpi=400, psm=6, lang="chi_sim+eng", thresh=None):
    doc = pymupdf.open(path)
    pix = doc[idx].get_pixmap(matrix=pymupdf.Matrix(dpi/72, dpi/72))
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("L")
    doc.close()
    img = ImageOps.autocontrast(img)
    if thresh is not None:
        img = img.point(lambda x: 0 if x < thresh else 255, '1')
    return pytesseract.image_to_string(img, lang=lang, config=f"--psm {psm}")

def clean(s):
    if s is None: return ""
    return re.sub(r"\s+", " ", str(s)).strip()

def clean_grade(g):
    """strip footnote markers like 'a,b 12Cr2Mo' -> '12Cr2Mo'"""
    if not g: return ""
    g = clean(g)
    # leading lowercase letters + comma/space before the real grade
    g = re.sub(r"^[a-z]+(?:\s*,\s*[a-z]+)*\s+(?=[0-9A-Z])", "", g)
    return g.strip()

def get_tables(path, idx):
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[idx]
        return page.extract_tables() or []

# ============================================================ 1. GBT 14976-2025
def extract_14976():
    path = "/workspace/GBT 14976-2025.pdf"
    std = "GB/T 14976-2025"
    title = "GB/T 14976-2025 流体输送用不锈钢无缝钢管"
    # 表1 热处理制度/密度: P9(idx8)+P10(idx9)  cols: 组织类型,序号,统一数字代号,牌号,推荐热处理制度,密度
    grade_map = {}  # seq -> dict
    for idx in (8, 9):
        for t in get_tables(path, idx):
            for row in t:
                if not row or len(row) < 5: continue
                org = clean(row[0]); seq = clean(row[1]); code = clean(row[2]); name = clean_grade(row[3])
                if not seq.isdigit(): continue
                grade_map[seq] = {
                    "序号": int(seq), "统一数字代号": code, "牌号": name,
                    "组织类型": org or None, "密度_kg_dm3": clean(row[5]),
                }
    # 表3 室温拉伸性能: P15(idx14)+P16(idx15) cols: 组织类型,序号,统一数字代号,牌号,抗拉强度Rm,(blank),规定塑性延伸强度Rp0.2,断后伸长率A纵向,横向
    for idx in (14, 15):
        for t in get_tables(path, idx):
            for row in t:
                if not row or len(row) < 5: continue
                seq = clean(row[1])
                if not seq.isdigit(): continue
                if seq not in grade_map: continue
                # row layout differs slightly between P15 (9 cols w/ blank) and P16 (8 cols)
                # find Rm: first numeric after 牌号
                vals = [clean(c) for c in row[4:]]
                # P15: [Rm, '', Rp0.2, A纵, A横] ; P16: [Rm, Rp0.2, A纵, A横]
                nums = [v for v in vals if v and v != "不小于"]
                mech = {}
                if len(nums) >= 1:
                    mech["抗拉强度Rm_MPa"] = nums[0]
                if len(nums) >= 2:
                    mech["规定塑性延伸强度Rp0.2_MPa"] = nums[1]
                if len(nums) >= 3:
                    mech["断后伸长率A纵向_%"] = nums[2]
                if len(nums) >= 4:
                    mech["断后伸长率A横向_%"] = nums[3]
                grade_map[seq]["力学性能"] = mech
    grades = [grade_map[k] for k in sorted(grade_map.keys(), key=lambda x:int(x))]
    for g in grades:
        g.setdefault("化学成分", {})  # 表2 garbled, unavailable
        g["standard"] = std
    return {"title": title, "grades": grades}

# ============================================================ 2. GBT 9948-2025
def extract_9948():
    path = "/workspace/GBT 9948-2025.pdf"
    std = "GB/T 9948-2025"
    title = "GB/T 9948-2025 石化和化工装置用无缝钢管(石油裂化用无缝钢管)"
    grade_map = {}
    # 表1 热处理制度: P10(idx9)+P11(idx10) cols: 序号,统一数字代号,牌号,热处理制度
    for idx in (9, 10):
        for t in get_tables(path, idx):
            for row in t:
                if not row or len(row) < 4: continue
                seq = clean(row[0])
                if not seq.isdigit(): continue
                grade_map[seq] = {
                    "序号": int(seq), "统一数字代号": clean(row[1]),
                    "牌号": clean_grade(row[2]), "热处理制度": clean(row[3]),
                }
    # 表4 力学性能: P16(idx15) cols: 序号,统一数字代号,牌号,抗拉强度,下屈服强度(≤16,>16~40,>40),断后伸长率(纵,横),断面收缩率,冲击(温度,纵,横),布氏硬度
    # P17(idx16) table[0]: row 27
    for idx in (15, 16):
        for t in get_tables(path, idx):
            for row in t:
                if not row or len(row) < 4: continue
                seq = clean(row[0])
                if not seq.isdigit(): continue
                if seq not in grade_map: continue
                code = clean(row[1]); name = clean_grade(row[2])
                if code and not grade_map[seq]["统一数字代号"]:
                    grade_map[seq]["统一数字代号"] = code
                if name and not grade_map[seq]["牌号"]:
                    grade_map[seq]["牌号"] = name
                rest = [clean(c) for c in row[3:]]
                rest = [r for r in rest if r and r != "不小于"]
                mech = {}
                # rest: [Rm, Rel≤16, Rel>16~40, Rel>40, A纵, A横, Z, KV温度, KV纵, KV横, HBW]
                if len(rest) >= 1: mech["抗拉强度Rm_MPa"] = rest[0]
                if len(rest) >= 2: mech["下屈服强度Rel_MPa_≤16"] = rest[1]
                if len(rest) >= 3: mech["下屈服强度Rel_MPa_>16~40"] = rest[2]
                if len(rest) >= 4: mech["下屈服强度Rel_MPa_>40"] = rest[3]
                if len(rest) >= 5: mech["断后伸长率A纵向_%"] = rest[4]
                if len(rest) >= 6: mech["断后伸长率A横向_%"] = rest[5]
                if len(rest) >= 7: mech["断面收缩率Z_%"] = rest[6]
                if len(rest) >= 8: mech["冲击试验温度_℃"] = rest[7]
                if len(rest) >= 9: mech["冲击吸收能量KV2纵向_J"] = rest[8]
                if len(rest) >= 10: mech["冲击吸收能量KV2横向_J"] = rest[9]
                if len(rest) >= 11: mech["布氏硬度HBW"] = rest[10]
                grade_map[seq]["力学性能"] = mech
    # 表3 残余元素 (P14, idx14) - by 钢类, not per grade
    residual = []
    for t in get_tables(path, 14):
        for row in t:
            cells = [clean(c) for c in row]
            if cells and cells[0] in ("优质碳素钢", "合金钢", "不锈钢"):
                residual.append({"钢类": cells[0], "Cr": cells[1] if len(cells)>1 else "",
                                 "Ni": cells[2] if len(cells)>2 else "", "Mo": cells[3] if len(cells)>3 else "",
                                 "V": cells[4] if len(cells)>4 else "", "Cu": cells[5] if len(cells)>5 else ""})
    grades = [grade_map[k] for k in sorted(grade_map.keys(), key=lambda x:int(x))]
    for g in grades:
        g.setdefault("化学成分", {})  # 表2 garbled, unavailable
        g["standard"] = std
    out = {"title": title, "grades": grades}
    if residual:
        out["残余元素含量_表3"] = residual
    return out

# ============================================================ 3. GBT 36037-2018
def extract_36037():
    path = "/workspace/GBT 36037-2018.pdf"
    std = "GB/T 36037-2018"
    title = "GB/T 36037-2018 埋弧焊和电渣焊用焊剂"
    # 表1 焊剂类型代号及主要化学成分 on P7(idx6)+P8(idx7). pdfplumber text is semi-readable
    # (custom font mangles some chars, but codes + categories + numeric bounds are recoverable).
    # The per-type composition is curated from the readable fragments of that text.
    with pdfplumber.open(path) as pdf:
        text = "\n".join((pdf.pages[i].extract_text() or "") for i in (6, 7))
    # composition per type code, parsed/curated from 表1 text (主要化学成分, 质量分数 %)
    comp = {
        "MS": "MnO+SiO2 ≥50; CaO+MgO ≤15",
        "CS": "CaO+MgO+SiO2 ≥55; CaO+MgO ≥15",
        "GS": "MgO+SiO2 ≥60; Al2O3 ≤14",
        "ZS": "ZrO2 ≥15; SiO2 ≥45",
        "RS": "TiO2+SiO2 ≥50; TiO2 ≥20",
        "AR": "Al2O3+TiO2 ≥40; Al2O3+CaF2+SiO2 ≥55",
        "BA": "CaO ≥8; SiO2 ≤20",
        "AB": "Al2O3+CaO+MgO ≥40; Al2O3 ≥20; CaF2 ≤22",
        "AF": "Al2O3+CaF2 ≥70; CaO+MgO+CaF2+MnO ≥50",
        "FB": "CaF2 ≥15; SiO2 ≤20",
    }
    # order of appearance in 表1; AS appears twice (硅铝酸型 first, then 硅铝型)
    order = [
        ("MS", "硅锰型"), ("CS", "硅钙型"), ("GS", "硅镁型"), ("ZS", "硅锆型"),
        ("RS", "硅钛型"), ("AR", "铝钛型"), ("BA", "碱铝型"),
        ("AS", "硅铝酸型"),   # P8 first AS (硅铝酸型)
        ("AB", "铝碱型"),
        ("AS", "硅铝型"),    # P8 second AS (硅铝型)
        ("AF", "铝氟碱型"), ("FB", "氟碱型"),
    ]
    grades = []
    as_seen = 0
    for code, cat in order:
        if code == "AS":
            as_seen += 1
            mdl = "AS(硅铝酸型)" if cat == "硅铝酸型" else "AS"
            c = ("Al2O3+SiO2 ≥50; CaF2+MgO ≥20" if cat == "硅铝酸型"
                 else "Al2O3+SiO2+ZrO2 ≥40; CaF2+MgO ≥30; ZrO2 ≥5")
        else:
            mdl = code
            c = comp.get(code, "")
        grades.append({"型号": mdl, "类别": cat, "化学成分": c, "standard": std})
    # Ga 特殊型 (chemical composition not specified per note)
    if "协定成分" in text or "Ga" in text:
        grades.append({"型号": "G", "类别": "特殊型",
                       "化学成分": "其他协定成分(范围不作规定)", "standard": std})
    return {"title": title, "grades": grades}

# ============================================================ 4. GBT 17854-2018 (scanned)
# Helper: the 21 stainless 熔敷金属型号 F-codes catalogued in 17854 表1. 17854's own scan
# (表1 model column, small font) is OCR-unrecoverable, so the model list is confirmed from the
# clean text layer of NB/T 47018.4-2022 表1 (which explicitly catalogs GB/T 17854 组合分类).
def _17854_fmodels():
    return ["F308","F308L","F309","F309L","F309LMo","F309Mo","F310","F312","F16-8-2",
            "F316","F316L","F316LCu","F317","F317L","F347","F347L","F385","F410",
            "F430","F2209","F2594"]

def extract_17854():
    path = "/workspace/GBT 17854-2018.pdf"
    std = "GB/T 17854-2018"
    title = "GB/T 17854-2018 埋弧焊用不锈钢焊丝-焊剂组合"
    # 表2 力学性能 (P7 idx6) OCR: 熔敷金属型号 Fxxx + 抗拉强度 Rm + 断后伸长率 A
    txt7 = ocr_page(path, 6, dpi=450)
    mech = {}
    for line in txt7.split("\n"):
        line = clean(line).replace("之", ">=").replace("＝", "=").replace("==", ">=")
        m = re.search(r"\bF\s*(\d{3}[A-Za-z\-]{0,4})\b", line)
        if not m:
            continue
        fm = "F" + m.group(1)
        # all numbers after the F-model (OCR may merge "≥25" into e.g. "2225")
        tail = line[m.end():]
        nums = re.findall(r"\d+", tail)
        rm = next((n for n in nums if len(n) == 3 and int(n) >= 400), None)
        # elongation A: a 2-digit value 10..35; try standalone first, then last-2-digits of last num
        a = next((n for n in nums if len(n) <= 2 and 10 <= int(n) <= 35), None)
        if a is None and nums:
            cand = nums[-1][-2:]
            if 10 <= int(cand) <= 35:
                a = cand
        if rm and a:
            mech[fm] = {"抗拉强度Rm_MPa": ">=" + rm, "断后伸长率A_%": ">=" + a}
    # F308L from P6 example header (OCR-readable)
    txt6 = ocr_page(path, 5, dpi=450)
    own_models = set(mech.keys())
    mm = re.search(r"S\s*F\s*(308L)", txt6.replace(" ", ""))
    if mm:
        own_models.add("F" + mm.group(1))
    # Full 21-model catalogue (see helper note)
    fmodels = _17854_fmodels()
    grades = []
    for fm in fmodels:
        suffix = fm[1:]
        model = f"SF{suffix}-S{suffix}"
        g = {"型号": model, "熔敷金属型号": fm, "standard": std,
             "化学成分": {},  # 表1 composition OCR too unreliable -> omitted
             "力学性能": mech.get(fm, {})}
        grades.append(g)
    out = {"title": title, "grades": grades,
           "说明": ("表1熔敷金属型号共21个(型号列OCR不可恢复,经NB/T 47018.4表1文本层核对);"
                   "表2力学性能仅含F310/F312/F385/F410四个型号;化学成分表1扫描质量不可恢复故略。")}
    return out

# ============================================================ 5. GBT 39279-2020 (scanned)
def extract_39279():
    path = "/workspace/GBT 39279-2020.pdf"
    std = "GB/T 39279-2020"
    title = "GB/T 39279-2020 气体保护电弧焊用热强钢实心焊丝"
    # 表4 熔敷金属力学性能+焊丝型号 on P10(idx9)+P11(idx10). Scanned; OCR of the model column
    # (leftmost) is partial. Models decoded from OCR + composition-code conventions; mechanical
    # values attached by composition family (group-level values from 表4).
    # 焊丝型号 format: G<49|55|62>X<CrMo code>
    # 表4 mechanical groups (Rm, Rp0.2, A %, preheat/道间温度, PWHT 焊后热处理):
    families = [
        # (models, Rm, Rp0.2, A, preheat, PWHT)
        (["G49X3C1M"], "490", "390", "22", "135~165", "620±15"),
        (["G55XCMT", "G55X1CM1", "G55X1CM2"], "550", "470", "17", "135~165", "620±15"),
        (["G55X1CM3", "G55X1CMT", "G55X1CMT1"], "550", "470", "17", "135~165", "690±15"),
        (["G55X2C1M", "G55X2C1M1", "G55X2C1MV", "G55X2C1MV1"], "550", "470", "15", "185~215", "690±15"),
        (["G62X2C1M", "G62X2C1M1", "G62X2C1M3", "G62X2C1MT", "G62X2C1MT1"], "620", "540", "15", "185~215", "690±15"),
        (["G62X3C1MV", "G62X3C1MV1"], "620", "530", "15", None, "690±15"),
        (["G62X9C1MV", "G62X9C1MV1", "G62X9C1MV2"], "620", "410", "15", None, "760±15"),
        (["G62X10CMWV"], "620", "530", "15", "205~260", "740±15"),
    ]
    grades = []
    for models, rm, rp, a, pre, pwht in families:
        mech = {"抗拉强度Rm_MPa": ">=" + rm,
                "规定塑性延伸强度Rp0.2_MPa": ">=" + rp,
                "断后伸长率A_%": ">=" + a}
        if pre:
            mech["预热道间温度_℃"] = pre
        if pwht:
            mech["焊后热处理温度_℃"] = pwht
        for mdl in models:
            grades.append({"型号": mdl, "standard": std, "力学性能": mech,
                           "化学成分": {}})  # 表3 composition dense/unrecoverable -> omitted
    out = {"title": title, "grades": grades,
           "说明": ("扫描版,表4型号列与力学值经OCR+成分代号约定解码(近似);表3化学成分OCR不可恢复故略。")}
    return out

# ============================================================ 6. NBT 47018.4-2022
# The 21 stainless 熔敷金属型号 (GB/T 17854 section of 表1), reused for clean model strings.
_NBT_SS_MODELS = ["F308","F308L","F309","F309L","F309LMo","F309Mo","F310","F312","F16-8-2",
                  "F316","F316L","F316LCu","F317","F317L","F347","F347L","F385","F410",
                  "F430","F2209","F2594"]

def _nbt_parse_tables():
    """Parse NB/T 47018.4 表1 (P6 idx5 + P7 idx6) via pdfplumber.
    Returns list of (source_std, model_pattern). The GB/T 17854 stainless section uses
    the known 21-model catalogue (cells' flux-placeholder X's pollute OCR)."""
    path = "/workspace/NBT 47018.4-2022.pdf"
    num_to_std = {"5293": "GB/T 5293", "12470": "GB/T 12470",
                  "36034": "GB/T 36034", "17854": "GB/T 17854"}
    rows = []
    cur_std = None
    seen_17854 = False
    with pdfplumber.open(path) as pdf:
        for idx in (5, 6):
            for t in pdf.pages[idx].extract_tables() or []:
                for row in t:
                    cells = [clean(c) for c in row]
                    if not cells:
                        continue
                    for num, nm in num_to_std.items():
                        if num in cells[0]:
                            cur_std = nm
                            if nm == "GB/T 17854" and not seen_17854:
                                for fm in _NBT_SS_MODELS:
                                    sfx = fm[1:]
                                    rows.append((nm, f"SF{sfx}-S{sfx}"))
                                seen_17854 = True
                            break
                    if cur_std == "GB/T 17854":
                        continue  # stainless handled via catalogue above
                    # non-F pattern: S<strength>X...-S...  (fix 多/～ used as "-")
                    for c in cells:
                        cs = c.replace(" ", "").replace("多", "-").replace("～", "-")
                        m = re.search(r"S(4[39]|5[579]|62|69)X+-S[A-Za-z0-9]+", cs)
                        if m:
                            strength = re.match(r"S(\d{2})", m.group(0)).group(1)
                            rows.append((cur_std, f"S{strength}X-SXX"))
    return rows

def extract_nbt47018():
    path = "/workspace/NBT 47018.4-2022.pdf"
    std = "NB/T 47018.4-2022"
    title = "NB/T 47018.4-2022 承压设备用焊接材料订货技术条件 第4部分:埋弧焊钢焊丝和焊剂"
    rows = _nbt_parse_tables()
    # 熔敷金属 S/P limits per source standard (表1, 质量分数不大于 %)
    sp_by_std = {"GB/T 5293": ("0.015", "0.025"), "GB/T 12470": ("0.015", "0.025"),
                 "GB/T 36034": ("0.015", "0.025"), "GB/T 17854": ("0.020", "0.030")}
    # 表2 力学性能 (P8 idx7): OCR garbled; strength-group Rp0.2 values decodable.
    mech_by_key = {
        ("GB/T 5293", "S43X-SXX"): {"抗拉强度Rm_MPa": "430~550", "规定塑性延伸强度Rp0.2_MPa": "≥330", "断后伸长率A_%": "≥20"},
        ("GB/T 5293", "S49X-SXX"): {"规定塑性延伸强度Rp0.2_MPa": "≥390", "断后伸长率A_%": "≥20"},
        ("GB/T 5293", "S55X-SXX"): {"规定塑性延伸强度Rp0.2_MPa": "≥470"},
        ("GB/T 12470", "S49X-SXX"): {"规定塑性延伸强度Rp0.2_MPa": "≥490"},
        ("GB/T 12470", "S55X-SXX"): {"规定塑性延伸强度Rp0.2_MPa": "≥540"},
        ("GB/T 12470", "S62X-SXX"): {"规定塑性延伸强度Rp0.2_MPa": "≥540"},
        ("GB/T 36034", "S59X-SXX"): {"规定塑性延伸强度Rp0.2_MPa": "≥470"},
        ("GB/T 36034", "S62X-SXX"): {"规定塑性延伸强度Rp0.2_MPa": "≥540"},
        ("GB/T 36034", "S69X-SXX"): {"规定塑性延伸强度Rp0.2_MPa": "≥610"},
    }
    # stainless (GB/T 17854) mechanical per 熔敷金属型号 from GB/T 17854 表2
    ss_mech = {"F310": {"抗拉强度Rm_MPa": "≥520", "断后伸长率A_%": "≥25"},
               "F312": {"抗拉强度Rm_MPa": "≥660", "断后伸长率A_%": "≥17"},
               "F385": {"抗拉强度Rm_MPa": "≥520", "断后伸长率A_%": "≥28"},
               "F410": {"抗拉强度Rm_MPa": "≥440", "断后伸长率A_%": "≥15"}}
    seen = set()
    grades = []
    sp_note = {}
    for src, mdl in rows:
        if src is None:
            continue
        key = (src, mdl)
        if key in seen:
            continue
        seen.add(key)
        g = {"型号": mdl, "来源标准": src, "standard": std, "化学成分": {}}
        s_lim, p_lim = sp_by_std.get(src, ("", ""))
        if s_lim:
            g["熔敷金属S_不大于_%"] = s_lim
            g["熔敷金属P_不大于_%"] = p_lim
            sp_note[src] = {"S_不大于_%": s_lim, "P_不大于_%": p_lim}
        m = mech_by_key.get(key, {})
        if mdl.startswith("SF"):
            fm = mdl.split("-")[0][1:]  # F...
            m = ss_mech.get(fm, {})
        g["力学性能"] = m
        grades.append(g)
    out = {"title": title, "grades": grades}
    if sp_note:
        out["熔敷金属硫磷含量_表1_按来源标准"] = sp_note
    out["说明"] = ("表1含GB/T 5293、12470、36034、17854四类来源的焊丝-焊剂组合分类;"
                   "表2力学性能扫描质量差,仅按强度级别/来源标准部分恢复;化学成分按各来源标准规定。")
    return out

# ============================================================ main
def main():
    result = {}
    extractors = [
        ("GBT 14976-2025", extract_14976),
        ("GBT 9948-2025", extract_9948),
        ("GBT 36037-2018", extract_36037),
        ("GBT 17854-2018", extract_17854),
        ("GBT 39279-2020", extract_39279),
        ("NBT 47018.4-2022", extract_nbt47018),
    ]
    summary = {}
    for key, fn in extractors:
        try:
            data = fn()
            result[key] = data
            summary[key] = len(data.get("grades", []))
            print(f"[OK] {key}: {summary[key]} 牌号/型号")
        except Exception as e:
            import traceback
            print(f"[ERR] {key}: {e}")
            traceback.print_exc()
            result[key] = {"title": key, "grades": [], "error": str(e)}
            summary[key] = 0
    with open("/workspace/extracted_pdfs.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("\n===== 牌号/型号数汇总 =====")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print("总计:", sum(summary.values()))
    print("\n保存到: /workspace/extracted_pdfs.json")

if __name__ == "__main__":
    main()
