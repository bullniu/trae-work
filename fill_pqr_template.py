"""
填充 PQR 模板：直接打开 PQR模板.docx，把焊接参数+知识库数据填入空格，
保留模板原有的一切格式（字体、表格、布局），只填空，不改模板。
"""
import re, sys, json, copy
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

TEMPLATE = "/workspace/PQR模板.docx"

# ---------- 工具函数 ----------
def _v(x, default=''):
    """安全取值，None/空 → default"""
    if x is None: return default
    s = str(x).strip()
    return s if s else default

def _vn(x, default=''):
    """数字取值，None/0/空 → default"""
    if x is None or x == '': return default
    try:
        f = float(x)
        if f == int(f): return str(int(f))
        return str(f)
    except: return _v(x, default)

def _date(s):
    if not s: return ''
    s = str(s).strip()
    if '-' in s:
        parts = s.split('-')
        if len(parts) >= 3:
            return f"{parts[0]}年{parts[1]}月{parts[2]}日"
        if len(parts) == 2:
            return f"{parts[0]}年{parts[1]}月"
    return s

def fill_after_label(para, label, value, replace_all_after=False):
    """在段落里把 'label：___' 中冒号后的空格替换为 value。
    replace_all_after=True 时，把 label 冒号后的全部内容（含示例值）替换为 value。
    保留 label 及段落第一个 run 的格式。"""
    if not para.runs:
        para.add_run(_v(label) + '：' + _v(value))
        return
    full = para.text
    if replace_all_after:
        # 替换 label 冒号后的全部内容
        pattern = re.escape(label) + r'\s*[：:]\s*.*$'
        new_text = f'{label}：{_v(value)}'
    else:
        pattern = re.escape(label) + r'\s*[：:]\s*'
        new_text = re.sub(pattern, f'{label}：{_v(value)}', full, count=1)
    if not re.search(pattern, full):
        return False
    if replace_all_after:
        new_text = re.sub(pattern, f'{label}：{_v(value)}', full, count=1)
    first = para.runs[0]
    for r in para.runs[1:]:
        r.text = ''
    first.text = new_text
    return True

def fill_after_sublabel(para, sublabel, value):
    """段落形如 '标题：___子标题___'，把子标题后的空格填为 value。
    用于"拉伸试验：___试验报告编号___"这种结构。"""
    if not para.runs: return
    full = para.text
    pattern = re.escape(sublabel) + r'\s*'
    if not re.search(pattern, full):
        return False
    new_text = re.sub(pattern, f'{sublabel}  {_v(value)}', full, count=1)
    first = para.runs[0]
    for r in para.runs[1:]:
        r.text = ''
    first.text = new_text
    return True

def set_cell_text(cell, value):
    """清空单元格所有段落，写入 value。保留第一个段落第一个 run 的格式。"""
    paras = cell.paragraphs
    if not paras:
        cell.add_paragraph(_v(value))
        return
    p0 = paras[0]
    # 取第一个 run 的 rPr 作为格式模板
    rpr_tmpl = None
    if p0.runs:
        rpr_el = p0.runs[0]._r.find(qn('w:rPr'))
        if rpr_el is not None:
            rpr_tmpl = copy.deepcopy(rpr_el)
    # 清空所有段落的 runs（保留段落本身）
    for p in paras:
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
    # 删除除第一段外的其他段落
    for p in paras[1:]:
        p._p.getparent().remove(p._p)
    # 在第一段写入值
    new_run = p0.add_run(_v(value))
    if rpr_tmpl is not None:
        # 复制字体格式
        new_rpr = copy.deepcopy(rpr_tmpl)
        new_run._r.insert(0, new_rpr)

def append_cell_line(cell, label, value):
    """在单元格末尾追加一行 'label：value'，复制上一段格式"""
    paras = cell.paragraphs
    tmpl_para = paras[-1] if paras else None
    rpr_tmpl = None
    if tmpl_para and tmpl_para.runs:
        rpr_el = tmpl_para.runs[0]._r.find(qn('w:rPr'))
        if rpr_el is not None:
            rpr_tmpl = copy.deepcopy(rpr_el)
    new_p = cell.add_paragraph()
    if tmpl_para is not None:
        # 复制段落属性 pPr
        ppr = tmpl_para._p.find(qn('w:pPr'))
        if ppr is not None:
            new_p._p.insert(0, copy.deepcopy(ppr))
    r = new_p.add_run(f'{label}：{_v(value)}')
    if rpr_tmpl is not None:
        r._r.insert(0, copy.deepcopy(rpr_tmpl))

def unique_cells(row):
    """返回去重后的 cell 列表（按物理 tc 元素）"""
    seen = set(); out = []
    for c in row.cells:
        cid = id(c._tc)
        if cid not in seen:
            seen.add(cid); out.append(c)
    return out


# ---------- 主填充函数 ----------
def fill_template(data, out_path):
    doc = Document(TEMPLATE)

    # 提取数据
    pqr = data.get('pqrForm', {})
    R = data.get('record', {})         # 焊接参数记录
    passes = R.get('passes', []) or data.get('passes', [])
    B1 = dict(data.get('baseMetal1', {}) or {})
    B2 = dict(data.get('baseMetal2', {}) or {})
    C = dict(data.get('consumable', {}) or {})
    coverage = data.get('coverage', {}) or {}

    # ===== 派生字段(知识库里没有,但模板需要) =====
    # 母材材料代号 = 类别号-组别号 (如 Fe-1-1)
    if not B1.get('materialCode') and B1.get('category'):
        g = B1.get('groupNo', '')
        B1['materialCode'] = f"{B1['category']}-{g}" if g != '' else B1['category']
    if not B2.get('materialCode') and B2.get('category'):
        g = B2.get('groupNo', '')
        B2['materialCode'] = f"{B2['category']}-{g}" if g != '' else B2['category']
    # 焊材金属材料代号 = F-No / A-No
    if not C.get('fillerMetalCode') and (C.get('fNo') or C.get('aNo')):
        C['fillerMetalCode'] = f"{C.get('fNo','')} / {C.get('aNo','')}".strip(' /')
    # 焊材填充金属类别 = fNo 或 category
    if not C.get('fillerCategory'):
        C['fillerCategory'] = C.get('fNo') or C.get('category') or ''

    # ===== 覆盖范围(基于规则计算的结果)优先于知识库固定范围 =====
    # coverage.thickness 是基于试件厚度+NB/T 47014 规则算出的"母材厚度覆盖范围"
    if coverage.get('thickness'):
        B1['buttThicknessRange'] = coverage['thickness']
    if coverage.get('weldMetal'):
        C['buttWeldMetalRange'] = coverage['weldMetal']
    # PWHT 规则文本
    if coverage.get('pwht') and not pqr.get('heatTreatTempRange'):
        pqr['heatTreatTempRange'] = coverage['pwht']

    pqrNo = _v(pqr.get('pqrNo'))
    pwpsNo = _v(pqr.get('pwpsNo'), pqrNo + '-W')
    unitName = _v(pqr.get('unitName'), '胜利油田胜机石油装备有限公司')
    weldMethod = _v(pqr.get('weldMethod'), R.get('weldMethod'))

    def calc_heat(p):
        """计算热输入 kJ/cm = I*U*η*60/(v*1000), v 单位 cm/min, SMAW η=0.8"""
        try:
            I = float(p.get('current') or 0)
            U = float(p.get('voltage') or 0)
            v = float(p.get('weldSpeed') or 0)
            eta = float(p.get('efficiency') or 0.8)
            if I and U and v:
                return f"{I*U*eta*60/(v*1000):.2f}"
        except: pass
        return ''

    tables = doc.tables

    # ============ 表0: PWPS 第1页 ============
    t0 = tables[0]
    # 行0: 单位名称（已填）+ 预焊接工艺规程编号
    fill_after_label(t0.rows[0].cells[0].paragraphs[1], '预焊接工艺规程编号', pwpsNo)
    # 行0 段0: 单位名称保留
    # 行1 左: 焊接接头 - 坡口形式（模板原有示例值 v 要一并替换）
    left_cell = unique_cells(t0.rows[1])[0]
    for p in left_cell.paragraphs:
        t = p.text
        if '坡口形式' in t:
            fill_after_label(p, '坡口形式', _v(pqr.get('grooveType')), replace_all_after=True)
        elif '衬垫' in t:
            fill_after_label(p, '衬垫（材料及规格）', f"{_v(pqr.get('gasketMaterial'),'/')}/{_v(pqr.get('gasketSize'),'/')}", replace_all_after=True)
    # 行2: 母材 - 类别号/组别号/标准号/材料代号/相焊
    bm_cell = t0.rows[2].cells[0]
    for p in bm_cell.paragraphs:
        t = p.text
        if '类别号' in t and '组别号' in t:
            # 段落含 "类别号  组别号  与类别号  组别号  相焊及标准号  材料代号  与标准号  材料代号  相焊"
            # 重建为填好值的形式
            new = (f"类别号  {_v(B1.get('category'))}  组别号  {_v(B1.get('groupNo'))}  "
                   f"与类别号  {_v(B2.get('category'))}  组别号  {_v(B2.get('groupNo'))}  相焊  "
                   f"及标准号  {_v(B1.get('standard'))}  材料代号  {_v(B1.get('materialCode'),'/')}  "
                   f"与标准号  {_v(B2.get('standard'))}  材料代号  {_v(B2.get('materialCode'),'/')}  相焊")
            if p.runs:
                for r in p.runs[1:]: r.text=''
                p.runs[0].text = new
        elif '厚度范围' in t:
            fill_after_label(p, '对接焊缝焊件母材厚度范围', _v(B1.get('buttThicknessRange')))
    # 行3: 填充金属
    fm_cell = t0.rows[3].cells[0]
    for p in fm_cell.paragraphs:
        t = p.text
        if '焊材类别' in t:
            fill_after_label(p, '焊材类别', _v(C.get('category')))
        elif '焊材标准' in t:
            fill_after_label(p, '焊材标准', _v(C.get('standard')))
        elif '填充金属尺寸' in t or '填充金属尺寸' in t:
            pass
        elif '焊材型号' in t:
            fill_after_label(p, '焊材型号', _v(C.get('modelNo')))
        elif '焊材牌号' in t:
            fill_after_label(p, '焊材牌号', _v(C.get('brand') or C.get('grade')))
        elif '金属材料代号' in t:
            fill_after_label(p, '金属材料代号', _v(C.get('fillerMetalCode'),'/'))
        elif '填充金属类别' in t:
            fill_after_label(p, '填充金属类别', _v(C.get('fillerCategory')))
        elif '对接焊缝焊件焊缝金属厚度范围' in t:
            fill_after_label(p, '对接焊缝焊件焊缝金属厚度范围', _v(C.get('buttWeldMetalRange')))
        elif '角焊缝焊件焊缝金属厚度范围' in t:
            fill_after_label(p, '角焊缝焊件焊缝金属厚度范围', _v(C.get('filletWeldMetalRange'),'/'))

    # ============ 表1: PWPS 第2页 ============
    t1 = tables[1]
    # 行0: 焊接位置/焊后热处理（左右两个大单元格）
    pos_cell = unique_cells(t1.rows[0])[0]
    for p in pos_cell.paragraphs:
        t = p.text
        if '对接焊缝的位置' in t:
            fill_after_label(p, '对接焊缝的位置', _v(pqr.get('buttWeldPos'),'平、横、立、仰'))
        elif '焊接方向' in t and '向上、向下' in t:
            # 多个焊接方向字段，重建
            new = f"焊接方向（向上、向下）  {_v(pqr.get('buttDirection'),'向上')}      角焊缝位置  {_v(pqr.get('filletWeldPos'),'平、横、立、仰')}      焊接方向（向上、向下）  {_v(pqr.get('filletDirection'),'向上')}"
            if p.runs:
                for r in p.runs[1:]: r.text=''
                p.runs[0].text = new
        elif '角焊缝位置' in t:
            fill_after_label(p, '角焊缝位置', _v(pqr.get('filletWeldPos'),'平、横、立、仰'))
    heat_cell = unique_cells(t1.rows[0])[1]
    for p in heat_cell.paragraphs:
        if '温度范围' in t:
            fill_after_label(p, '温度范围（℃）', _v(pqr.get('heatTreatTempRange'),'/'))
        elif '保温时间' in p.text:
            fill_after_label(p, '保温时间（h）', _v(pqr.get('heatTreatHoldTime'),'/'))

    # 行1: 预热 / 保护气体
    pre_cell = unique_cells(t1.rows[1])[0]
    for p in pre_cell.paragraphs:
        t = p.text
        if t.startswith('预热 (') or '预热 (℃)' in t:
            fill_after_label(p, '预热 (℃) (允许最低值)', _v(pqr.get('preheatMinTemp'),'/'))
        elif '层间温度' in t:
            fill_after_label(p, '层间温度(℃)(允许最高值)', _v(pqr.get('interpassMaxTemp'),'/'))
        elif '保持预热时间' in t:
            fill_after_label(p, '保持预热时间', _v(pqr.get('holdPreheatTime'),'/'))
        elif '加热方式' in t:
            fill_after_label(p, '加热方式', _v(pqr.get('heatingMethod'),'/'))
    gas_cell = unique_cells(t1.rows[1])[1]
    # 保护气/尾部/背面三行
    gas_paras = gas_cell.paragraphs
    gas_items = [
        ('保  护  气', 'shieldGas', 'shieldMix', 'shieldFlow'),
        ('尾部保护气', 'tailShieldGas', 'tailMix', 'tailFlow'),
        ('背面保护气', 'backShieldGas', 'backMix', 'backFlow'),
    ]
    for p in gas_paras:
        for label, gk, mk, fk in gas_items:
            if label in p.text:
                val = f"{_v(pqr.get(gk),'/')}     {_v(pqr.get(mk),'/')}     {_v(pqr.get(fk),'/')}"
                fill_after_label(p, label, val)

    # 行2: 电特性（电流种类/极性/焊接电流范围/电弧电压）
    elec_cell = t1.rows[2].cells[0]
    for p in elec_cell.paragraphs:
        t = p.text
        if '电流种类' in t:
            fill_after_label(p, '电流种类', _v(pqr.get('currentType'),'/'))
        elif '极性' in t and '极性：' in t:
            fill_after_label(p, '极性', _v(pqr.get('polarity'),'/'))
        elif '焊接电流范围' in t:
            fill_after_label(p, '焊接电流范围(A)', _v(pqr.get('currentRangeA'),'/'))
        elif '电弧电压(V)' in t or '电弧电压' in t:
            fill_after_label(p, '电弧电压(V)', _v(pqr.get('voltageRangeV'),'/'))

    # 行5-11: 多层多道数据（7行空行）
    pass_rows = t1.rows[5:12]  # 行5到11
    n_fill = min(len(passes), len(pass_rows))
    for i in range(n_fill):
        p = passes[i]
        cells = unique_cells(pass_rows[i])
        # 9列: 焊道/焊层 | 焊接方法 | 牌号 | 直径 | 极性 | 电流(A) | 电弧电压(V) | 焊接速度(cm/min) | 热输入(kJ/cm)
        vals = [
            f"{_v(p.get('layer'))}-{_v(p.get('passNo'))}",
            _v(p.get('weldMethod'), weldMethod),
            _v(p.get('consumable'), C.get('brand') or C.get('grade')),
            _v(p.get('consumableSpec'), C.get('depositSize') or C.get('depositSpec')),
            _v(pqr.get('polarity'),'DCEP'),
            _vn(p.get('current')),
            _vn(p.get('voltage')),
            _vn(p.get('weldSpeed')),
            calc_heat(p)
        ]
        for ci, val in enumerate(vals):
            if ci < len(cells):
                set_cell_text(cells[ci], val)

    # 行12: 钨极/喷嘴/熔滴/送丝
    tung_cell = t1.rows[12].cells[0]
    for p in tung_cell.paragraphs:
        t = p.text
        if '钨极类型及直径' in t:
            new = f"钨极类型及直径：{_v(pqr.get('tungstenTypeDia'),'/')}      喷嘴直径 (mm)：{_v(pqr.get('nozzleDia'),'/')}      熔滴过渡形式：{_v(pqr.get('metalTransferMode'),'/')}      焊丝送进速度 (cm/min)：{_v(pqr.get('wireFeedSpeed'),'/')}"
            if p.runs:
                for r in p.runs[1:]: r.text=''
                p.runs[0].text = new
    # 行13: 技术措施
    tech_cell = t1.rows[13].cells[0]
    for p in tech_cell.paragraphs:
        t = p.text
        if '摆动焊或不摆动焊' in t:
            new = f"摆动焊或不摆动焊：{_v(pqr.get('swingOrNot'),'/')}      摆动参数：{_v(pqr.get('swingParams'),'/')}      焊前清理和层间清理：{_v(pqr.get('preAndInterpassCleaning'),'/')}      背面清根方法：{_v(pqr.get('backGougeMethod'),'/')}      单道焊或多道焊每面：{_v(pqr.get('singleOrMultiPerSide'),'/')}      单丝焊或多丝焊：{_v(pqr.get('singleOrMultiWire'),'/')}      导电嘴至工件距离(mm)：{_v(pqr.get('contactTipDist'),'/')}      锤击：{_v(pqr.get('peening'),'/')}      其他：{_v(pqr.get('otherTechnical'),'/')}"
            if p.runs:
                for r in p.runs[1:]: r.text=''
                p.runs[0].text = new
    # 行14: 签字栏（编制/审核/批准+日期）
    sign_cells = unique_cells(t1.rows[14])
    # 12个独立单元格：编制|空|日期|空|审核|空|日期|空|批准|空|日期|空
    sign_map = {
        1: _v(pqr.get('compiler')),         # 编制后
        3: _date(pqr.get('compilerDate')),   # 编制日期后
        5: _v(pqr.get('auditor')),          # 审核后
        7: _date(pqr.get('auditorDate')),    # 审核日期后
        9: _v(pqr.get('approver')),         # 批准后
        11: _date(pqr.get('approverDate')),  # 批准日期后
    }
    for idx, val in sign_map.items():
        if idx < len(sign_cells):
            set_cell_text(sign_cells[idx], val)

    # ============ 表2: PQR 第1页 ============
    t2 = tables[2]
    # 行0: 单位名称（已填）+ 焊接工艺评定报告编号 + 预焊接工艺规程编号 + 焊接方法 + 机械化程度
    h0 = t2.rows[0].cells[0]
    for p in h0.paragraphs:
        t = p.text
        if '焊接工艺评定报告编号' in t:
            fill_after_label(p, '焊接工艺评定报告编号', pqrNo)
        elif '预焊接工艺规程编号' in t:
            fill_after_label(p, '预焊接工艺规程编号', pwpsNo)
        elif '焊接方法' in t:
            fill_after_label(p, '焊接方法', weldMethod)
        elif '机械化程度' in t:
            fill_after_label(p, '机械化程度(手工, 机动自动)', _v(pqr.get('mechanizationLevel'),'/'))

    # 行2-6 多个单元格：母材/焊后热处理/保护气体/填充金属/电特性/焊接位置/技术措施/预热
    # 行2 左: 母材 材料标准/钢号/类组别号/相焊/厚度/直径/其他
    bm_p = t2.rows[2].cells[0]
    for p in bm_p.paragraphs:
        t = p.text
        if '材料标准' in t:
            fill_after_label(p, '材料标准', _v(B1.get('standard')))
        elif '钢 号' in t:
            fill_after_label(p, '钢 号.', f"{_v(B1.get('grade'))} / {_v(B2.get('grade'))}")
        elif '与类、组别号' in t or ('类、组别号' in t and '相焊' in t):
            # 段落形如 "类、组别号：___ 与类、组别号：___ 相焊"，整体重建
            new = (f"类、组别号  {_v(B1.get('category'))} / {_v(B1.get('groupNo'))}  "
                   f"与类、组别号  {_v(B2.get('category'))} / {_v(B2.get('groupNo'))}  相焊")
            if p.runs:
                for r in p.runs[1:]: r.text=''
                p.runs[0].text = new
        elif '类、组别号' in t:
            fill_after_label(p, '类、组别号', f"{_v(B1.get('category'))} / {_v(B1.get('groupNo'))}")
        elif '厚 度' in t:
            fill_after_label(p, '厚 度', _v(B1.get('thicknessOrDia') or B1.get('buttThicknessRange')))
        elif '直 径' in t:
            fill_after_label(p, '直 径', '/')
        elif '其 他' in t:
            fill_after_label(p, '其 他', '/')

    # 行2 右: 焊后热处理
    ht_p = t2.rows[2].cells[1]
    for p in ht_p.paragraphs:
        t = p.text
        if '热处理温度' in t:
            fill_after_label(p, '热处理温度(℃)', _v(pqr.get('heatTreatTempRange'),'/'))
        elif '保温时间' in t:
            fill_after_label(p, '保温时间 (h)', _v(pqr.get('heatTreatHoldTime'),'/'))

    # 行3 右: 保护气体
    pg_p = t2.rows[3].cells[1]
    for label, gk, mk, fk in [('保  护  气','shieldGas','shieldMix','shieldFlow'),
                               ('尾部保护气','tailShieldGas','tailMix','tailFlow'),
                               ('背面保护气','backShieldGas','backMix','backFlow')]:
        for p in pg_p.paragraphs:
            if label in p.text:
                fill_after_label(p, label, f"{_v(pqr.get(gk),'/')}     {_v(pqr.get(mk),'/')}     {_v(pqr.get(fk),'/')}")

    # 行4 左: 填充金属
    fm_p = t2.rows[4].cells[0]
    for p in fm_p.paragraphs:
        t = p.text
        if '焊材标准' in t:
            fill_after_label(p, '焊材标准', _v(C.get('standard')))
        elif '焊材牌号' in t:
            fill_after_label(p, '焊材牌号', _v(C.get('brand') or C.get('grade')))
        elif '焊材规格' in t:
            fill_after_label(p, '焊材规格', _v(C.get('depositSize') or C.get('depositSpec')))
        elif '焊缝金属厚度' in t:
            fill_after_label(p, '焊缝金属厚度', _v(C.get('buttWeldMetalRange'),'/'))
        elif '其 他' in t:
            fill_after_label(p, '其 他', '/')

    # 行4 右: 电特性
    el_p = t2.rows[4].cells[1]
    for p in el_p.paragraphs:
        t = p.text
        if '电流种类' in t:
            fill_after_label(p, '电流种类', _v(pqr.get('currentType'),'/'))
        elif '极性' in t and '极性：' in t:
            fill_after_label(p, '极性', _v(pqr.get('polarity'),'/'))
        elif '钨极尺寸' in t:
            fill_after_label(p, '钨极尺寸', '/')
        elif '焊接电流' in t:
            fill_after_label(p, '焊接电流 (A)', _v(pqr.get('currentRangeA'),'/'))
        elif '电弧电压' in t:
            fill_after_label(p, '电弧电压 (V)', _v(pqr.get('voltageRangeV'),'/'))
        elif '最大热输入' in t:
            fill_after_label(p, '其他最大热输入', _v(pqr.get('maxHeatInput'),'/'))

    # 行5 左: 焊接位置
    wp_p = t2.rows[5].cells[0]
    for p in wp_p.paragraphs:
        t = p.text
        if '对接焊缝位置' in t:
            new = f"对接焊缝位置  {_v(pqr.get('buttWeldPos'),'平位')}  方向(向上, 向下) {_v(pqr.get('buttDirection'),'/')}"
            if p.runs:
                for r in p.runs[1:]: r.text=''
                p.runs[0].text = new
        elif '角焊缝位置' in t:
            new = f"角焊缝位置  {_v(pqr.get('filletWeldPos'),'/')}  方向(向上, 向下) {_v(pqr.get('filletDirection'),'/')}"
            if p.runs:
                for r in p.runs[1:]: r.text=''
                p.runs[0].text = new

    # 行5 右: 技术措施
    tc_p = t2.rows[5].cells[1]
    for p in tc_p.paragraphs:
        t = p.text
        if '焊接速度' in t:
            fill_after_label(p, '焊接速度(cm/min)', _v(pqr.get('weldSpeed'),'/'))
        elif '摆动或不摆动' in t:
            fill_after_label(p, '摆动或不摆动', _v(pqr.get('swingOrNot'),'/'))
        elif '摆动参数' in t:
            fill_after_label(p, '摆动参数', _v(pqr.get('swingParams'),'/'))
        elif '多道焊或单道焊每面' in t:
            fill_after_label(p, '多道焊或单道焊每面', _v(pqr.get('singleOrMultiPerSide'),'/'))
        elif '多丝焊或单丝焊' in t:
            fill_after_label(p, '多丝焊或单丝焊', _v(pqr.get('singleOrMultiWire'),'/'))
        elif '其他' in t and '技术措施' not in t:
            fill_after_label(p, '其他', _v(pqr.get('otherTechnical'),'/'))

    # 行6 左: 预热
    ph_p = t2.rows[6].cells[0]
    for p in ph_p.paragraphs:
        t = p.text
        if '预热温度' in t:
            fill_after_label(p, '预热温度(℃)', _v(pqr.get('preheatMinTemp'),'/'))
        elif '层间温度' in t:
            fill_after_label(p, '层间温度 (℃)', _v(pqr.get('interpassMaxTemp'),'/'))
        elif '其他' in t and '预热' not in t:
            fill_after_label(p, '其他', _v(pqr.get('heatingMethod'),'/'))

    # ============ 表3: PQR 第2页（拉伸/弯曲/冲击/金相/无损/签字） ============
    t3 = tables[3]
    # 行0: 拉伸试验报告编号（段落形如"拉伸试验：___试验报告编号___"，填试验报告编号后的值）
    for p in t3.rows[0].cells[0].paragraphs:
        if '拉伸试验' in p.text and '试验报告编号' in p.text:
            fill_after_sublabel(p, '试验报告编号', _v(pqr.get('tensileReportNo')))
    # 行2-7: 拉伸数据（6行×6列）
    tensile_rows = pqr.get('tensileRows', []) or []
    for i in range(6):
        r = tensile_rows[i] if i < len(tensile_rows) else {}
        cells = unique_cells(t3.rows[2+i])
        # 6列: 试样编号 | 截面尺寸 | 横截面积 | 断裂载荷 | 抗拉强度 | 断裂部位和特征
        vals = [
            _v(r.get('no')),
            f"{_vn(r.get('sizeW'))}×{_vn(r.get('sizeT'))}" if r.get('sizeW') else '',
            _vn(r.get('area')),
            _vn(r.get('fractureLoad')),
            _vn(r.get('rm')),
            _v(r.get('fracturePos'))
        ]
        for ci, val in enumerate(vals):
            if ci < len(cells):
                set_cell_text(cells[ci], val)
    # 行8: 弯曲试验报告编号
    for p in t3.rows[8].cells[0].paragraphs:
        if '弯曲试验' in p.text and '试验报告编号' in p.text:
            fill_after_sublabel(p, '试验报告编号', _v(pqr.get('bendReportNo')))
    # 行10-13: 弯曲数据（4行×6列）
    bend_rows = pqr.get('bendRows', []) or []
    for i in range(4):
        r = bend_rows[i] if i < len(bend_rows) else {}
        cells = unique_cells(t3.rows[10+i])
        # 6列: 试样编号 | 试样类型及件数 | 试样厚度 | 弯心直径 | 弯曲角度 | 试验结果
        vals = [
            _v(r.get('no')),
            _v(r.get('typeAndCount')),
            _vn(r.get('thickness')),
            _vn(r.get('mandrelDia')),
            _vn(r.get('angle')),
            _v(r.get('result'))
        ]
        for ci, val in enumerate(vals):
            if ci < len(cells):
                set_cell_text(cells[ci], val)
    # 行14: 冲击试验报告编号
    for p in t3.rows[14].cells[0].paragraphs:
        if '冲击试验' in p.text and '试验报告编号' in p.text:
            fill_after_sublabel(p, '试验报告编号', _v(pqr.get('charpyReportNo')))
    # 行17-18: 冲击数据（2行×9列）
    charpy_rows = pqr.get('charpyRows', []) or []
    for i in range(2):
        r = charpy_rows[i] if i < len(charpy_rows) else {}
        cells = unique_cells(t3.rows[17+i])
        # 9列: 试样编号 | 试样尺寸 | 缺口类型 | 缺口位置 | 试验温度 | 1 | 2 | 3 | 标准值
        vals = [
            _v(r.get('no')),
            f"{_vn(r.get('sizeW'))}×{_vn(r.get('sizeT'))}" if r.get('sizeW') else '',
            _v(r.get('notchType')),
            _v(r.get('notchPos')),
            _vn(r.get('testTemp')),
            _vn(r.get('akv1')),
            _vn(r.get('akv2')),
            _vn(r.get('akv3')),
            ''  # 标准值留空
        ]
        for ci, val in enumerate(vals):
            if ci < len(cells):
                set_cell_text(cells[ci], val)
    # 行19: 金相检验报告编号
    for p in t3.rows[19].cells[0].paragraphs:
        if '金相检验' in p.text and '检验报告编号' in p.text:
            fill_after_sublabel(p, '检验报告编号', _v(pqr.get('metallographyReportNo')))
    # 行21: 焊脚差（横跨6格）
    weld_foot = _v(pqr.get('weldFootDiff'))
    foot_cells = unique_cells(t3.rows[21])
    if len(foot_cells) > 1:
        set_cell_text(foot_cells[1], weld_foot)
    # 行22: 无损检测报告编号
    for p in t3.rows[22].cells[0].paragraphs:
        if '无损检测' in p.text and '检测报告编号' in p.text:
            fill_after_sublabel(p, '检测报告编号', _v(pqr.get('ndtReportNo')))
    # 行23: 无损检测结果（1个大单元格）
    ndt_text = f"RT {_v(pqr.get('rtResult'),'无裂纹')}        UT {_v(pqr.get('utResult'),'/')}        MT {_v(pqr.get('mtResult'),'/')}        PT {_v(pqr.get('ptResult'),'/')}        其他 {_v(pqr.get('otherNdt'),'/')}"
    set_cell_text(t3.rows[23].cells[0], ndt_text)
    # 行24: 附加说明
    add_p = t3.rows[24].cells[0]
    for p in add_p.paragraphs:
        if '附加说明' in p.text:
            fill_after_label(p, '附加说明', _v(pqr.get('conclusionText')))
    # 行26: 焊工/焊工代号/施焊日期
    wk_cells = unique_cells(t3.rows[26])
    # 6格: 焊工|空|焊工代号|空|施焊日期|空
    if len(wk_cells) >= 6:
        set_cell_text(wk_cells[1], _v(pqr.get('welder')))
        set_cell_text(wk_cells[3], _v(pqr.get('welderCode')))
        set_cell_text(wk_cells[5], _date(pqr.get('weldDate')))
    # 行27-28: 编制/审核/批准 + 日期
    sign27 = unique_cells(t3.rows[27])
    sign28 = unique_cells(t3.rows[28])
    if len(sign27) >= 6 and len(sign28) >= 6:
        set_cell_text(sign27[1], _v(pqr.get('compiler')))
        set_cell_text(sign27[3], _v(pqr.get('auditor')))
        set_cell_text(sign27[5], _v(pqr.get('approver')))
        set_cell_text(sign28[1], _date(pqr.get('compilerDate')))
        set_cell_text(sign28[3], _date(pqr.get('auditorDate')))
        set_cell_text(sign28[5], _date(pqr.get('approverDate')))

    # ============ 表4: 施焊记录 ============
    t4 = tables[4]
    # 行0: 指导书编号
    cells0 = unique_cells(t4.rows[0])
    # 结构: 焊接工艺评定施焊记录(×10)|指导书编号(×6)|空(×4)
    if len(cells0) >= 4:
        # cells0[2] 是"指导书编号"，cells0[3] 是空格
        set_cell_text(cells0[3], pwpsNo)
    # 行1: 记录编号
    cells1 = unique_cells(t4.rows[1])
    if len(cells1) >= 4:
        set_cell_text(cells1[3], pqrNo + '-R')
    # 行2: 焊接方法|施焊位置|设备型号|电源种类和极性
    cells2 = unique_cells(t4.rows[2])
    # 结构: 焊接方法(×7)|空|施焊位置(×3)|空|设备型号(×6)|空|电源种类和极性(×4)|空
    # 找空格填值
    # cells2 逻辑: [焊接方法, 空, 施焊位置, 空, 设备型号, 空, 电源种类和极性, 空]
    if len(cells2) >= 8:
        set_cell_text(cells2[1], weldMethod)
        set_cell_text(cells2[3], _v(pqr.get('buttWeldPos'),'平位'))
        set_cell_text(cells2[5], _v(pqr.get('equipModel'),'/'))
        set_cell_text(cells2[7], f"{_v(pqr.get('currentType'),'/')} / {_v(pqr.get('polarity'),'/')}")

    # 后续行: 试件钢号/规格/批号/材料标记/坡口形式/焊材牌号/规格/...
    # 由于表4行数较多且结构复杂，按文本标签定位填值
    for ri in range(3, len(t4.rows)):
        cells = unique_cells(t4.rows[ri])
        for ci, cell in enumerate(cells):
            txt = cell.paragraphs[0].text if cell.paragraphs else ''
            # 跳过表头行（含标签的）
            if any(k in txt for k in ['焊接层次','焊材','焊接电流','电弧电压','焊接速度','线能量']):
                continue
            # 检验记录等，按需填
    # 施焊记录的多层多道表：找到含"焊接层次"的行，其下空行填数据
    for ri in range(len(t4.rows)):
        cells = unique_cells(t4.rows[ri])
        hdr = ' '.join(c.paragraphs[0].text for c in cells if c.paragraphs)
        if '焊接层次' in hdr and '焊材' in hdr:
            # 这是表头，下面是数据行
            data_start = ri + 1
            # 6列: 焊接层次|焊材/规格|焊接电流A|电弧电压V|焊接速度cm/min|线能量kJ/cm
            for i in range(min(len(passes), 8)):
                if data_start + i >= len(t4.rows): break
                p = passes[i]
                dcells = unique_cells(t4.rows[data_start + i])
                vals = [
                    f"{_v(p.get('layer'))}-{_v(p.get('passNo'))}",
                    f"{_v(p.get('consumable'), C.get('brand') or C.get('grade'))} / {_v(p.get('consumableSpec'), C.get('depositSize') or C.get('depositSpec'))}",
                    _vn(p.get('current')),
                    _vn(p.get('voltage')),
                    _vn(p.get('weldSpeed')),
                    calc_heat(p)
                ]
                for ci, val in enumerate(vals):
                    if ci < len(dcells):
                        set_cell_text(dcells[ci], val)
            break

    # 保存
    doc.save(out_path)
    return out_path


# ---------- 测试 ----------
if __name__ == '__main__':
    test_data = {
        "pqrForm": {
            "pqrNo": "PQR-2024-001", "pwpsNo": "PWPS-2024-001",
            "unitName": "胜利油田胜机石油装备有限公司",
            "weldMethod": "SMAW", "grooveType": "V",
            "currentType": "DC", "polarity": "DCEP",
            "currentRangeA": "90-120", "voltageRangeV": "20-24",
            "buttWeldPos": "平位", "filletWeldPos": "/",
            "compiler": "张三", "auditor": "李四", "approver": "王五",
            "compilerDate": "2024-01-15", "auditorDate": "2024-01-16", "approverDate": "2024-01-17",
            "welder": "赵六", "welderCode": "W001", "weldDate": "2024-01-10",
            "tensileReportNo": "T-001", "bendReportNo": "B-001", "charpyReportNo": "C-001",
            "ndtReportNo": "N-001",
            "tensileRows": [{"no":"T1","sizeW":10,"sizeT":5,"area":50,"fractureLoad":25,"rm":500,"fracturePos":"焊缝"}],
            "bendRows": [{"no":"B1","typeAndCount":"面弯2件","thickness":5,"mandrelDia":20,"angle":180,"result":"合格"}],
            "charpyRows": [{"no":"C1","sizeW":10,"sizeT":5,"notchType":"V","notchPos":"HAZ","testTemp":-20,"akv1":50,"akv2":52,"akv3":48}],
            "rtResult": "无裂纹", "utResult":"/", "mtResult":"/", "ptResult":"/",
            "conclusionText": "本评定按NB/T 47014-2023规定执行，各项指标合格。",
            "weldFootDiff": "0.5"
        },
        "record": {"weldMethod": "SMAW"},
        "passes": [
            {"layer":1,"passNo":1,"weldMethod":"SMAW","consumable":"J422","consumableSpec":"Φ3.2","current":100,"voltage":22,"weldSpeed":8,"efficiency":0.8},
            {"layer":2,"passNo":1,"weldMethod":"SMAW","consumable":"J422","consumableSpec":"Φ4.0","current":120,"voltage":24,"weldSpeed":10,"efficiency":0.8}
        ],
        "baseMetal1": {"standard":"GB/T 700","grade":"Q235B","category":"I","groupNo":"1","materialCode":"Fe-1","buttThicknessRange":"3-20","thicknessOrDia":"6"},
        "baseMetal2": {"standard":"GB/T 700","grade":"Q235B","category":"I","groupNo":"1","materialCode":"Fe-1","buttThicknessRange":"3-20"},
        "consumable": {"standard":"GB/T 5117","brand":"J422","grade":"E4303","depositSize":"Φ3.2","depositSpec":"Φ3.2","category":"碳钢焊条","buttWeldMetalRange":"≤20","fillerCategory":"Fe-1"}
    }
    out = fill_template(test_data, "/workspace/test_filled.docx")
    print(f"已生成: {out}")
    import os
    print(f"文件大小: {os.path.getsize(out)} bytes")
