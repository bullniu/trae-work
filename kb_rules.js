/**
 * 焊接工艺评定知识库 - 评定规则库
 * 依据:NB/T 47014-2023《承压设备焊接工艺评定》
 * 核心内容:母材分类表、焊材分类表、试件厚度→覆盖范围规则
 *
 * 数据结构:
 *   baseMetalCategory  母材类别号-组别号-标准 映射表
 *   consumableCategory 焊材 F-No. + A-No. 分类表
 *   thicknessRule      试件厚度→覆盖母材厚度范围 规则
 *   weldMetalRule      试件焊缝金属厚度→覆盖熔敷金属厚度 规则
 *   categoryMatchRule  母材类别相焊适用规则
 *   pwhtRule           焊后热处理规则
 */
window.KB_RULES = {
  // ============ 1. 母材分类表(NB/T 47014 附录C) ============
  // 类别号-组别号 含义 + 典型牌号示例
  baseMetalCategory: {
    'Fe-1': {
      desc: '碳钢',
      groups: {
        '1': { desc:'碳钢,屈服强度 ≤295 MPa', examples:'Q235,Q245R,20,20G,10,L245', standards:'GB/T 700, GB/T 713.2, GB/T 699, GB/T 5310, GB/T 9948, GB/T 9711' },
        '2': { desc:'碳钢,屈服强度 >295 MPa', examples:'Q275,35,45,L415,Q255', standards:'GB/T 700, GB/T 699, GB/T 9711' }
      }
    },
    'Fe-2': {
      desc: '低合金钢',
      groups: {
        '1': { desc:'低合金钢,Cr≤0.50%,Mo≤0.20%,Cu≤0.50%,无其他合金', examples:'Q355,Q390,Q370R', standards:'GB/T 1591, GB/T 713.5' },
        '2': { desc:'低合金钢,Cr>0.50%或Mo>0.20%或含其他合金', examples:'Q420,Q460', standards:'GB/T 1591' },
        '3': { desc:'低合金钢,沉淀硬化', examples:'—', standards:'GB/T 1591' }
      }
    },
    'Fe-3': {
      desc: '低合金耐热钢(Cr-Mo)',
      groups: {
        '1': { desc:'Cr≤0.50%,Mo≤0.50%', examples:'12CrMoG,15CrMoG', standards:'GB/T 5310, GB/T 9948' },
        '2': { desc:'Cr 0.50%-2.00%,Mo 0.50%-1.00%', examples:'12Cr1MoVG,12Cr2MoG,15Cr1Mo1G', standards:'GB/T 5310, GB/T 9948' },
        '3': { desc:'Cr 2.00%-3.00%,Mo 1.00%-1.50%', examples:'—', standards:'GB/T 5310, GB/T 9948' }
      }
    },
    'Fe-4': {
      desc: '低合金耐热钢(高Cr)',
      groups: {
        '1': { desc:'Cr 3.00%-9.00%,Mo≤1.00%或不含Mo', examples:'10Cr9Mo1VNbN(P91/T91)', standards:'GB/T 5310' },
        '2': { desc:'Cr 9.00%-12.00%,含V/Nb/N', examples:'—', standards:'GB/T 5310' }
      }
    },
    'Fe-4A': { desc:'马氏体不锈钢(承压设备简化分类)', groups:{ '1':{ desc:'11-13Cr马氏体', examples:'06Cr13,12Cr13,20Cr13', standards:'GB/T 1220' } } },
    'Fe-5A': { desc:'马氏体不锈钢', groups:{ '1':{ desc:'410系(11-13Cr)', examples:'06Cr13,12Cr13,20Cr13', standards:'GB/T 1220' } } },
    'Fe-5B': { desc:'马氏体不锈钢(沉淀硬化)', groups:{ '1':{ desc:'17-4PH等', examples:'05Cr17Ni4Cu4Nb', standards:'GB/T 1220' } } },
    'Fe-6': { desc:'沉淀硬化不锈钢', groups:{ '1':{ desc:'17-7PH等', examples:'06Cr17Ni7Al', standards:'GB/T 1220' } } },
    'Fe-7A': {
      desc: '铁素体不锈钢',
      groups: {
        '1': { desc:'11-14Cr铁素体', examples:'06Cr13Al,022Cr12,06Cr13', standards:'GB/T 4238' },
        '2': { desc:'11-13Cr含Ni铁素体', examples:'022Cr12Ni', standards:'GB/T 4238' }
      }
    },
    'Fe-7B': { desc:'铁素体不锈钢(高Cr)', groups:{ '1':{ desc:'14-30Cr铁素体', examples:'06Cr13Al', standards:'GB/T 4238' } } },
    'Fe-8': {
      desc: '奥氏体不锈钢',
      groups: {
        '1': { desc:'Cr 16-22%,Ni 8-14%,Mo≤3%', examples:'06Cr19Ni10(304),022Cr19Ni10(304L),06Cr17Ni12Mo2(316)', standards:'GB/T 14976-2025, GB/T 4238' },
        '2': { desc:'Cr 22-28%,Ni 14-32%,Mo≤3%', examples:'06Cr25Ni20(310),16Cr25Ni20Si2(310s)', standards:'GB/T 14976-2025' }
      }
    },
    'Fe-9A': { desc:'Ni合金钢(低Ni)', groups:{ '1':{ desc:'2.5%Ni钢', examples:'2.5Ni', standards:'—' } } },
    'Fe-9B': { desc:'Ni合金钢(高Ni)', groups:{ '1':{ desc:'3.5%Ni钢', examples:'3.5Ni', standards:'—' } } },
    'Fe-10A': { desc:'奥氏体-铁素体双相不锈钢', groups:{ '1':{ desc:'Cr 18-23%,Ni 3-8%', examples:'022Cr19Ni5Mo3Si2N', standards:'GB/T 4238' } } },
    'Fe-10B': { desc:'奥氏体-铁素体双相不锈钢(高Cr)', groups:{ '1':{ desc:'Cr 23-29%,Ni 4-9%', examples:'022Cr25Ni6Mo2N', standards:'GB/T 4238' } } },
    'Fe-10H': { desc:'镍基合金(Ni≥35%)', groups:{ '1':{ desc:'Ni基固溶', examples:'NS312(Inconel600),NS334(C-276),NS336(625)', standards:'GB/T 15011' } } },
    'Fe-10I': { desc:'镍基合金(含Cu)', groups:{ '1':{ desc:'Ni-Cu型', examples:'Monel 400', standards:'GB/T 15011' } } },
    'Fe-10J': { desc:'镍基合金(沉淀硬化)', groups:{ '1':{ desc:'时效强化型', examples:'—', standards:'GB/T 15011' } } },
    'Fe-10K': { desc:'镍基合金(特种)', groups:{ '1':{ desc:'—', examples:'—', standards:'—' } } }
  },

  // ============ 2. 焊材分类表(NB/T 47014 附录D) ============
  consumableCategory: {
    // F-No. 按药皮/焊剂类型分类(焊条用)
    fNo: {
      'F-1': { desc:'埋弧焊、电渣焊焊剂类', appliesTo:'焊剂(SJ/HJ)', commonBrands:'SJ431, SJ101, HJ431' },
      'F-2': { desc:'不锈钢用焊剂类', appliesTo:'不锈钢焊剂', commonBrands:'—' },
      'F-3': { desc:'碳钢、低合金钢用焊条类(非低氢)', appliesTo:'碳钢/低合金钢焊条(钛型/钛钙型/钛铁矿型/氧化铁型)', commonBrands:'J421,J422,J502,J507' },
      'F-4': { desc:'低合金钢用焊条类(低氢)', appliesTo:'低合金耐热钢焊条(低氢型)', commonBrands:'R307,R317,R407' },
      'F-5': { desc:'不锈钢用焊条类(低氢)', appliesTo:'不锈钢低氢焊条', commonBrands:'A402(部分)' },
      'F-6': { desc:'不锈钢用焊条类(非低氢)', appliesTo:'不锈钢焊条(钛钙型/钛型)', commonBrands:'A002,A102,A132,A302' },
      'F-22': { desc:'气保焊用焊丝类', appliesTo:'不锈钢/低合金钢焊丝', commonBrands:'ER308L,ER316L,ER50-6' },
      'F-23': { desc:'埋弧焊用焊丝类', appliesTo:'碳钢/低合金钢焊丝', commonBrands:'H08A,H08MnA,H10Mn2' }
    },
    // A-No. 按熔敷金属化学成分分类(全焊材)
    aNo: {
      'A-1': { desc:'碳钢', typicalComp:'C≤0.20%,Mn 0.60-1.60%,Si≤0.80%', appliesTo:'碳钢焊材', commonBrands:'J422,J507,ER50-6,H08A' },
      'A-2': { desc:'低合金钢(含Mo/Cr-Mo)', typicalComp:'Mn 0.50-1.50%,Cr 0.40-2.50%,Mo 0.40-1.20%', appliesTo:'低合金耐热钢焊材', commonBrands:'J557,R307,R317,R407,ER55-B2' },
      'A-3': { desc:'低合金钢(Cr-Mo-V)', typicalComp:'Cr 1.00-1.50%,Mo 0.40-0.70%,V 0.10-0.40%', appliesTo:'低合金耐热钢焊材', commonBrands:'R312,R317,H08CrMoVA' },
      'A-4': { desc:'低合金钢(Mn-Mo)', typicalComp:'Mn 1.20-1.80%,Mo 0.25-0.55%', appliesTo:'低合金钢焊材', commonBrands:'J606,J607' },
      'A-5': { desc:'低合金钢(Ni)', typicalComp:'Ni 0.50-2.50%', appliesTo:'低温钢焊材', commonBrands:'—' },
      'A-8': { desc:'不锈钢(奥氏体)', typicalComp:'Cr 18-25%,Ni 8-22%', appliesTo:'奥氏体不锈钢焊材', commonBrands:'A002,A102,A302,ER308L' },
      'A-9': { desc:'不锈钢(马氏体)', typicalComp:'Cr 11-13%,Ni<2.50%', appliesTo:'马氏体不锈钢焊材', commonBrands:'—' },
      'A-10': { desc:'不锈钢(铁素体)', typicalComp:'Cr 11-30%,Ni<2.50%', appliesTo:'铁素体不锈钢焊材', commonBrands:'—' }
    }
  },

  // ============ 3. 试件厚度→覆盖母材厚度范围 规则 ============
  // NB/T 47014-2023 第6.3条:对接焊缝、试件厚度 t → 覆盖范围
  // 公式依据:表5(对接焊缝)与表7(角焊缝)
  // key 为母材类别号,'通用' 为默认规则
  thicknessRule: {
    '通用': {
      rule: 't ≤ 3 mm → 覆盖 0.5t ~ 2t (且 ≥0.5mm);\nt = 3-12 mm → 覆盖 0.5t ~ 2t;\nt = 12-100 mm → 覆盖 0.5t ~ 2t;\nt > 100 mm → 覆盖 0.5t ~ 1.5t',
      formula: (t) => {
        const tf = parseFloat(t);
        if (isNaN(tf)) return '需输入试件厚度';
        if (tf <= 0) return '无效';
        if (tf <= 3) return `${Math.max(0.5, (0.5*tf).toFixed(1))} ~ ${(2*tf).toFixed(1)} mm (最小0.5mm)`;
        if (tf <= 12) return `${(0.5*tf).toFixed(1)} ~ ${(2*tf).toFixed(1)} mm`;
        if (tf <= 100) return `${(0.5*tf).toFixed(1)} ~ ${(2*tf).toFixed(1)} mm`;
        return `${(0.5*tf).toFixed(1)} ~ ${(1.5*tf).toFixed(1)} mm`;
      }
    },
    'Fe-8': {
      rule: '奥氏体不锈钢:\nt ≤ 10 mm → 覆盖 0.5t ~ 2t;\nt = 10-38 mm → 覆盖 0.5t ~ 2t;\nt > 38 mm → 覆盖 0.5t ~ 2t',
      formula: (t) => {
        const tf = parseFloat(t);
        if (isNaN(tf)) return '需输入试件厚度';
        if (tf <= 0) return '无效';
        return `${(0.5*tf).toFixed(1)} ~ ${(2*tf).toFixed(1)} mm`;
      }
    },
    'Fe-10H': {
      rule: '镍基合金:\nt ≤ 10 mm → 覆盖 0.5t ~ 2t;\nt > 10 mm → 覆盖 0.5t ~ 2t',
      formula: (t) => {
        const tf = parseFloat(t);
        if (isNaN(tf)) return '需输入试件厚度';
        return `${(0.5*tf).toFixed(1)} ~ ${(2*tf).toFixed(1)} mm`;
      }
    }
  },

  // ============ 4. 试件焊缝金属厚度→覆盖熔敷金属厚度 规则 ============
  // NB/T 47014-2023 第6.4条:w 为试件焊缝金属厚度
  weldMetalRule: {
    '通用': {
      rule: 'w ≤ 1.5 mm → 覆盖 ≤ 2w;\n1.5 < w ≤ 10 mm → 覆盖 0.5w ~ 2w;\nw > 10 mm → 覆盖 0.5w ~ 2w (最小1.5mm)',
      formula: (w) => {
        const wf = parseFloat(w);
        if (isNaN(wf)) return '需输入焊缝金属厚度';
        if (wf <= 0) return '无效';
        if (wf <= 1.5) return `≤ ${(2*wf).toFixed(1)} mm`;
        return `${Math.max(1.5, (0.5*wf).toFixed(1))} ~ ${(2*wf).toFixed(1)} mm`;
      }
    }
  },

  // ============ 5. 母材类别相焊适用规则(NB/T 47014 第6.2条) ============
  // 同类母材:评定覆盖相同类别-组别
  // 异类母材:必须分别评定,但同类别号不同组别可覆盖
  categoryMatchRule: {
    sameCategory: {
      rule: '同一类别号、任一组别号的母材相焊,评定覆盖同一类别号、任一组别号',
      example: 'Fe-1-1 / Fe-1-1 评定覆盖 Fe-1-1 / Fe-1-1, Fe-1-1 / Fe-1-2, Fe-1-2 / Fe-1-2',
      applies: '同类相焊,使用焊材A-No相同'
    },
    diffGroupSameCategory: {
      rule: '不同类别号母材相焊,必须分别评定,无覆盖',
      example: 'Fe-1 与 Fe-2 相焊,需 Fe-1/Fe-2 专项评定',
      applies: '异类相焊,焊材按强度匹配/化学成分匹配'
    },
    diffCategory: {
      rule: '不同类别号母材相焊,任一侧评定均不得覆盖另一侧',
      example: 'Fe-8(304)与 Fe-1(Q235)相焊,需 Fe-8/Fe-1 专项评定,可使用A-8焊材',
      applies: '异种钢焊接,选过渡层焊材(A-8如A302)'
    },
    weldMetalCategoryRule: {
      rule: '焊缝金属熔敷金属类别(A-No)相同者,任一评定覆盖另一;\nA-No不同需分别评定',
      example: 'A-1焊材评定覆盖其他A-1焊材;A-1与A-2不互覆盖',
      applies: '焊材替换规则'
    }
  },

  // ============ 6. 焊后热处理规则(NB/T 47014 第6.5条) ============
  pwhtRule: {
    rule: '评定应覆盖产品焊后热处理状态,且保温时间不低于产品保温时间的80%\n试件PWHT保温时间 t_h → 覆盖产品 0.8×t_h ~ ∞',
    byCategory: {
      'Fe-1': '一般不强制PWHT;厚度>40mm或设计要求时进行 600-650℃ 回火',
      'Fe-2': '厚度>30mm或设计要求时 PWHT 580-620℃',
      'Fe-3': '强制PWHT:600-680℃(按Cr-Mo含量);焊后立即消氢 250-350℃×2h',
      'Fe-4': '强制PWHT:730-780℃;焊后立即消氢 250-350℃×2h',
      'Fe-5A': '可淬火+回火:980-1030℃油淬+650-750℃回火;焊后及时回火防裂',
      'Fe-7A': '退火 700-780℃;通常焊后不热处理',
      'Fe-8': '固溶 1000-1150℃水冷;通常焊后不热处理,含Ti/Nb稳定化元素时 850-900℃稳定化'
    }
  },

  // ============ 7. 焊接位置规则(NB/T 47014 第6.6条) ============
  positionRule: {
    rule: '对接焊缝:1G(平)评定覆盖 1G、1F;2G(横)覆盖 1G/2G/1F/2F;\n2FR(横转)覆盖 1G/2FR/1F/2F;\n5G(立)、6G(斜立)各覆盖本位置+所有平/横/角\n立向下焊(5GX/6GX)覆盖立向下',
    table: {
      '1G':  { covers:['1G','1F'], desc:'平焊' },
      '2G':  { covers:['1G','2G','1F','2F'], desc:'横焊' },
      '2FR': { covers:['1G','2FR','1F','2F'], desc:'横转焊(管转动)' },
      '5G':  { covers:['1G','2G','5G','1F','2F','4F'], desc:'立焊' },
      '6G':  { covers:['1G','2G','5G','6G','1F','2F','4F','6F'], desc:'斜立焊(45°管)' },
      '6GR': { covers:['1G','2G','5G','6G','6GR','1F','2F','4F','6F'], desc:'45°管+限制' }
    }
  },

  // ============ 8. 管径规则 ============
  pipeRule: {
    rule: '管对接焊缝评定:\n试件外径 D ≤ 60 mm → 覆盖 0.5D ~ 2D (最小10mm);\nD > 60 mm → 覆盖 0.5D ~ ∞\n板材对接评定可覆盖管材 D ≥ 150 mm 的对接焊缝',
    formula: (d) => {
      const df = parseFloat(d);
      if (isNaN(df)) return '需输入管外径';
      if (df <= 0) return '无效';
      if (df <= 60) return `${Math.max(10, (0.5*df).toFixed(1))} ~ ${(2*df).toFixed(1)} mm`;
      return `${(0.5*df).toFixed(1)} mm ~ ∞`;
    }
  }
};
