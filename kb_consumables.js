/**
 * 焊接工艺评定知识库 - 焊材库
 * 依据:GB/T 5117、GB/T 5118、GB/T 8110、GB/T 5293、GB/T 36037、NB/T 47018 系列、GB/T 17854 等
 * 字段:
 *   brand        牌号(国内牌号 J/E 等)
 *   model        型号(GB/T 标准型号 E43xx / ER50-x 等)
 *   category     焊材类别(NB/T 47014 F-No. + A-No. 联合分类)
 *   fNo         NB/T 47014 F-No.
 *   aNo         NB/T 47014 A-No.
 *   standard     所属标准号
 *   type         类型(碳钢焊条/低合金钢焊条/不锈钢焊条/焊丝/焊剂等)
 *   depositSize  常用规格(mm)
 *   composition  熔敷金属化学成分(%)
 *   tensile      熔敷金属力学性能
 *   remarks      说明
 */
window.KB_CONSUMABLES = [
  // ============ 碳钢焊条 GB/T 5117 ============
  { brand:'J421', model:'E4313', fNo:'F-3', aNo:'A-1', category:'碳钢焊条', standard:'GB/T 5117', type:'钛型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.12',Mn:'0.30-0.60',Si:'≤0.35',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥420',Rel:'≥330',A:'≥22'}, remarks:'氧化钛型药皮,易起弧' },
  { brand:'J422', model:'E4303', fNo:'F-3', aNo:'A-1', category:'碳钢焊条', standard:'GB/T 5117', type:'钛钙型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.12',Mn:'0.30-0.60',Si:'≤0.25',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥420',Rel:'≥330',A:'≥22'}, remarks:'最常用碳钢焊条' },
  { brand:'J423', model:'E4301', fNo:'F-3', aNo:'A-1', category:'碳钢焊条', standard:'GB/T 5117', type:'钛铁矿型', depositSize:'Φ3.2/4.0/5.0', composition:{C:'≤0.12',Mn:'0.35-0.60',Si:'≤0.25',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥420',Rel:'≥330',A:'≥22'} },
  { brand:'J424', model:'E4320', fNo:'F-3', aNo:'A-1', category:'碳钢焊条', standard:'GB/T 5117', type:'氧化铁型', depositSize:'Φ3.2/4.0/5.0', composition:{C:'≤0.12',Mn:'0.50-0.90',Si:'≤0.15',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥420',Rel:'≥330',A:'≥22'} },
  { brand:'J425', model:'E4311', fNo:'F-3', aNo:'A-1', category:'碳钢焊条', standard:'GB/T 5117', type:'高纤维素钾型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.12',Mn:'0.35-0.60',Si:'≤0.15',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥420',Rel:'≥330',A:'≥22'}, remarks:'立向下焊' },
  { brand:'J426', model:'E4316', fNo:'F-3', aNo:'A-1', category:'碳钢焊条', standard:'GB/T 5117', type:'低氢钾型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.12',Mn:'1.25',Si:'≤0.90',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥420',Rel:'≥330',A:'≥22'}, remarks:'低氢型' },
  { brand:'J427', model:'E4315', fNo:'F-3', aNo:'A-1', category:'碳钢焊条', standard:'GB/T 5117', type:'低氢钠型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.12',Mn:'1.25',Si:'≤0.90',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥420',Rel:'≥330',A:'≥22'}, remarks:'低氢型,重要结构' },
  // 碳钢焊条≥490
  { brand:'J502', model:'E5003', fNo:'F-3', aNo:'A-1', category:'碳钢焊条', standard:'GB/T 5117', type:'钛钙型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.12',Mn:'0.60-1.20',Si:'≤0.30',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥500',Rel:'≥400',A:'≥20'} },
  { brand:'J503', model:'E5001', fNo:'F-3', aNo:'A-1', category:'碳钢焊条', standard:'GB/T 5117', type:'钛铁矿型', depositSize:'Φ3.2/4.0', composition:{C:'≤0.12',Mn:'0.60-1.20',Si:'≤0.30',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥500',Rel:'≥400',A:'≥20'} },
  { brand:'J505', model:'E5011', fNo:'F-3', aNo:'A-1', category:'碳钢焊条', standard:'GB/T 5117', type:'高纤维素钾型', depositSize:'Φ3.2/4.0', composition:{C:'≤0.12',Mn:'0.60-1.20',Si:'≤0.30',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥500',Rel:'≥400',A:'≥20'}, remarks:'立向下焊' },
  { brand:'J506', model:'E5016', fNo:'F-3', aNo:'A-1', category:'碳钢焊条', standard:'GB/T 5117', type:'低氢钾型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.12',Mn:'1.60',Si:'≤0.90',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥500',Rel:'≥400',A:'≥22'}, remarks:'常用低氢' },
  { brand:'J507', model:'E5015', fNo:'F-3', aNo:'A-1', category:'碳钢焊条', standard:'GB/T 5117', type:'低氢钠型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.12',Mn:'1.60',Si:'≤0.90',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥500',Rel:'≥400',A:'≥22'}, remarks:'重要结构常用' },

  // ============ 低合金钢焊条 GB/T 5118 ============
  { brand:'J556', model:'E5516-G', fNo:'F-3', aNo:'A-2', category:'低合金钢焊条', standard:'GB/T 5118', type:'低氢钾型', depositSize:'Φ3.2/4.0', composition:{C:'≤0.12',Mn:'1.00-1.75',Si:'≤0.60',Mo:'0.40-0.65',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥550',Rel:'≥440',A:'≥20'}, remarks:'低合金耐热' },
  { brand:'J557', model:'E5515-G', fNo:'F-3', aNo:'A-2', category:'低合金钢焊条', standard:'GB/T 5118', type:'低氢钠型', depositSize:'Φ3.2/4.0', composition:{C:'≤0.12',Mn:'1.00-1.75',Si:'≤0.60',Mo:'0.40-0.65',S:'≤0.035',P:'≤0.040'}, tensile:{Rm:'≥550',Rel:'≥440',A:'≥20'} },
  { brand:'J606', model:'E6016-G', fNo:'F-3', aNo:'A-2', category:'低合金钢焊条', standard:'GB/T 5118', type:'低氢钾型', depositSize:'Φ3.2/4.0', composition:{C:'≤0.12',Mn:'1.25-1.80',Si:'≤0.60',Mo:'0.25-0.45',S:'≤0.035',P:'≤0.035'}, tensile:{Rm:'≥600',Rel:'≥530',A:'≥17'} },
  { brand:'J607', model:'E6015-G', fNo:'F-3', aNo:'A-2', category:'低合金钢焊条', standard:'GB/T 5118', type:'低氢钠型', depositSize:'Φ3.2/4.0', composition:{C:'≤0.12',Mn:'1.25-1.80',Si:'≤0.60',Mo:'0.25-0.45',S:'≤0.035',P:'≤0.035'}, tensile:{Rm:'≥600',Rel:'≥530',A:'≥17'} },
  { brand:'J707', model:'E7015-G', fNo:'F-3', aNo:'A-2', category:'低合金钢焊条', standard:'GB/T 5118', type:'低氢钠型', depositSize:'Φ3.2/4.0', composition:{C:'≤0.12',Mn:'1.25-1.80',Si:'≤0.60',Mo:'0.25-0.45',Ni:'0.80-1.20',S:'≤0.035',P:'≤0.035'}, tensile:{Rm:'≥690',Rel:'≥590',A:'≥16'} },
  // 耐热钢焊条
  { brand:'R202', model:'E5503-B1', fNo:'F-3', aNo:'A-2', category:'低合金耐热钢焊条', standard:'GB/T 5118', type:'钛钙型', depositSize:'Φ3.2/4.0', composition:{C:'0.05-0.12',Mn:'0.90',Si:'0.30',Cr:'0.40-0.65',Mo:'0.40-0.60'}, tensile:{Rm:'≥540',Rel:'≥440',A:'≥17'}, remarks:'Cr0.5Mo0.5' },
  { brand:'R207', model:'E5515-B1', fNo:'F-3', aNo:'A-2', category:'低合金耐热钢焊条', standard:'GB/T 5118', type:'低氢钠型', depositSize:'Φ3.2/4.0', composition:{C:'0.05-0.12',Mn:'0.90',Si:'0.30',Cr:'0.40-0.65',Mo:'0.40-0.60'}, tensile:{Rm:'≥540',Rel:'≥440',A:'≥17'} },
  { brand:'R302', model:'E5503-B2', fNo:'F-3', aNo:'A-2', category:'低合金耐热钢焊条', standard:'GB/T 5118', type:'钛钙型', depositSize:'Φ3.2/4.0', composition:{C:'0.05-0.12',Mn:'0.90',Si:'0.30',Cr:'1.00-1.50',Mo:'0.40-0.65'}, tensile:{Rm:'≥540',Rel:'≥440',A:'≥17'}, remarks:'1Cr0.5Mo' },
  { brand:'R307', model:'E5515-B2', fNo:'F-3', aNo:'A-2', category:'低合金耐热钢焊条', standard:'GB/T 5118', type:'低氢钠型', depositSize:'Φ3.2/4.0', composition:{C:'0.05-0.12',Mn:'0.90',Si:'0.30',Cr:'1.00-1.50',Mo:'0.40-0.65'}, tensile:{Rm:'≥540',Rel:'≥440',A:'≥17'}, remarks:'15CrMo常用' },
  { brand:'R312', model:'E5503-B2-V', fNo:'F-3', aNo:'A-2', category:'低合金耐热钢焊条', standard:'GB/T 5118', type:'钛钙型', depositSize:'Φ3.2/4.0', composition:{C:'0.05-0.12',Mn:'0.90',Cr:'1.00-1.50',Mo:'0.40-0.65',V:'0.10-0.35'}, tensile:{Rm:'≥540',Rel:'≥440',A:'≥17'} },
  { brand:'R317', model:'E5515-B2-V', fNo:'F-3', aNo:'A-2', category:'低合金耐热钢焊条', standard:'GB/T 5118', type:'低氢钠型', depositSize:'Φ3.2/4.0', composition:{C:'0.05-0.12',Mn:'0.90',Cr:'1.00-1.50',Mo:'0.40-0.65',V:'0.10-0.35'}, tensile:{Rm:'≥540',Rel:'≥440',A:'≥17'}, remarks:'12Cr1MoV常用' },
  { brand:'R402', model:'E6000-B3', fNo:'F-3', aNo:'A-2', category:'低合金耐热钢焊条', standard:'GB/T 5118', type:'钛钙型', depositSize:'Φ3.2/4.0', composition:{C:'0.05-0.12',Mn:'0.90',Cr:'2.00-2.50',Mo:'0.90-1.20'}, tensile:{Rm:'≥590',Rel:'≥490',A:'≥15'}, remarks:'2.25Cr1Mo' },
  { brand:'R407', model:'E6015-B3', fNo:'F-3', aNo:'A-2', category:'低合金耐热钢焊条', standard:'GB/T 5118', type:'低氢钠型', depositSize:'Φ3.2/4.0', composition:{C:'0.05-0.12',Mn:'0.90',Cr:'2.00-2.50',Mo:'0.90-1.20'}, tensile:{Rm:'≥590',Rel:'≥490',A:'≥15'}, remarks:'12Cr2Mo常用' },

  // ============ 不锈钢焊条 GB/T 983(对应A-No) ============
  { brand:'A002', model:'E308L-16', fNo:'F-6', aNo:'A-8', category:'不锈钢焊条', standard:'GB/T 983', type:'钛钙型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.04',Cr:'18.00-21.00',Ni:'9.00-12.00',Mn:'0.50-2.50',Si:'≤0.90'}, tensile:{Rm:'≥515',A:'≥35'}, remarks:'304L用' },
  { brand:'A022', model:'E316L-16', fNo:'F-6', aNo:'A-8', category:'不锈钢焊条', standard:'GB/T 983', type:'钛钙型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.04',Cr:'17.00-20.00',Ni:'11.00-14.00',Mo:'2.00-3.00',Mn:'0.50-2.50'}, tensile:{Rm:'≥515',A:'≥30'}, remarks:'316L用' },
  { brand:'A102', model:'E308-16', fNo:'F-6', aNo:'A-8', category:'不锈钢焊条', standard:'GB/T 983', type:'钛钙型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.08',Cr:'18.00-21.00',Ni:'9.00-12.00',Mn:'0.50-2.50',Si:'≤0.90'}, tensile:{Rm:'≥550',A:'≥35'}, remarks:'304用' },
  { brand:'A132', model:'E347-16', fNo:'F-6', aNo:'A-8', category:'不锈钢焊条', standard:'GB/T 983', type:'钛钙型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.08',Cr:'18.00-21.00',Ni:'9.00-13.00',Nb:'8×C-1.00',Mn:'0.50-2.50'}, tensile:{Rm:'≥520',A:'≥30'}, remarks:'321/347用' },
  { brand:'A232', model:'E316-16', fNo:'F-6', aNo:'A-8', category:'不锈钢焊条', standard:'GB/T 983', type:'钛钙型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.08',Cr:'18.00-21.00',Ni:'9.00-13.00',Mo:'2.00-3.00',Mn:'0.50-2.50'}, tensile:{Rm:'≥520',A:'≥30'}, remarks:'316用' },
  { brand:'A302', model:'E309-16', fNo:'F-6', aNo:'A-8', category:'不锈钢焊条', standard:'GB/T 983', type:'钛钙型', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.15',Cr:'22.00-25.00',Ni:'12.00-14.00',Mn:'0.50-2.50',Si:'≤0.90'}, tensile:{Rm:'≥550',A:'≥25'}, remarks:'异种钢焊接' },
  { brand:'A402', model:'E310-15', fNo:'F-6', aNo:'A-8', category:'不锈钢焊条', standard:'GB/T 983', type:'低氢钠型', depositSize:'Φ3.2/4.0', composition:{C:'≤0.20',Cr:'25.00-28.00',Ni:'20.00-22.50',Mn:'1.00-2.50',Si:'≤0.75'}, tensile:{Rm:'≥550',A:'≥25'}, remarks:'310耐热用' },

  // ============ 气保焊焊丝 GB/T 8110 ============
  { brand:'ER50-6', model:'ER50-6', fNo:'F-6', aNo:'A-1', category:'碳钢气保焊丝', standard:'GB/T 8110', type:'实芯焊丝', depositSize:'Φ1.0/1.2/1.6', composition:{C:'0.06-0.15',Mn:'1.40-1.85',Si:'0.80-1.15',S:'≤0.035',P:'≤0.025'}, tensile:{Rm:'≥500',Rel:'≥420',A:'≥22'}, remarks:'GMAW常用' },
  { brand:'ER49-1', model:'ER49-1', fNo:'F-6', aNo:'A-1', category:'碳钢气保焊丝', standard:'GB/T 8110', type:'实芯焊丝', depositSize:'Φ1.0/1.2/1.6', composition:{C:'≤0.11',Mn:'1.80-2.10',Si:'0.65-0.95',S:'≤0.030',P:'≤0.030'}, tensile:{Rm:'≥490',Rel:'≥372',A:'≥23'} },
  { brand:'ER55-B2', model:'ER55-B2', fNo:'F-6', aNo:'A-2', category:'低合金耐热钢气保焊丝', standard:'GB/T 8110', type:'实芯焊丝', depositSize:'Φ1.0/1.2/1.6', composition:{C:'0.07-0.12',Mn:'0.40-0.70',Cr:'1.20-1.50',Mo:'0.40-0.65',Si:'0.40-0.70'}, tensile:{Rm:'≥550',Rel:'≥440',A:'≥19'}, remarks:'15CrMo用' },
  { brand:'ER55-B2MnV', model:'ER55-B2-MnV', fNo:'F-6', aNo:'A-2', category:'低合金耐热钢气保焊丝', standard:'GB/T 8110', type:'实芯焊丝', depositSize:'Φ1.0/1.2/1.6', composition:{C:'0.06-0.12',Mn:'0.75-1.05',Cr:'1.20-1.50',Mo:'0.40-0.65',V:'0.20-0.40'}, tensile:{Rm:'≥550',Rel:'≥440',A:'≥19'}, remarks:'12Cr1MoV用' },
  { brand:'ER62-B3', model:'ER62-B3', fNo:'F-6', aNo:'A-2', category:'低合金耐热钢气保焊丝', standard:'GB/T 8110', type:'实芯焊丝', depositSize:'Φ1.0/1.2/1.6', composition:{C:'0.07-0.12',Mn:'0.40-0.70',Cr:'2.30-2.70',Mo:'0.90-1.20',Si:'0.40-0.70'}, tensile:{Rm:'≥620',Rel:'≥530',A:'≥17'}, remarks:'12Cr2Mo用' },
  { brand:'ER308L', model:'ER308L', fNo:'F-6', aNo:'A-8', category:'不锈钢气保焊丝', standard:'GB/T 4241', type:'实芯焊丝', depositSize:'Φ1.0/1.2/1.6', composition:{C:'≤0.030',Cr:'19.50-22.00',Ni:'9.00-11.00',Mn:'1.00-2.50',Si:'0.30-0.65'}, tensile:{Rm:'≥520'}, remarks:'304L用' },
  { brand:'ER316L', model:'ER316L', fNo:'F-6', aNo:'A-8', category:'不锈钢气保焊丝', standard:'GB/T 4241', type:'实芯焊丝', depositSize:'Φ1.0/1.2/1.6', composition:{C:'≤0.030',Cr:'18.00-20.00',Ni:'11.00-14.00',Mo:'2.00-3.00',Mn:'1.00-2.50'}, tensile:{Rm:'≥520'}, remarks:'316L用' },
  { brand:'ER309', model:'ER309', fNo:'F-6', aNo:'A-8', category:'不锈钢气保焊丝', standard:'GB/T 4241', type:'实芯焊丝', depositSize:'Φ1.0/1.2/1.6', composition:{C:'≤0.08',Cr:'23.00-25.00',Ni:'12.00-14.00',Mn:'1.00-2.50'}, tensile:{Rm:'≥550'}, remarks:'异种钢用' },

  // ============ 埋弧焊焊丝 GB/T 5293 / GB/T 12470 ============
  { brand:'H08A', model:'H08A', fNo:'F-6', aNo:'A-1', category:'碳钢埋弧焊丝', standard:'GB/T 5293-2018', type:'实芯焊丝', depositSize:'Φ2.5/3.2/4.0/5.0', composition:{C:'≤0.10',Mn:'0.30-0.55',Si:'≤0.03',S:'≤0.025',P:'≤0.025'}, tensile:{Rm:'410-550'}, remarks:'配焊剂SJ431' },
  { brand:'H08E', model:'H08E', fNo:'F-6', aNo:'A-1', category:'碳钢埋弧焊丝', standard:'GB/T 5293-2018', type:'实芯焊丝', depositSize:'Φ2.5/3.2/4.0', composition:{C:'≤0.10',Mn:'0.30-0.55',Si:'≤0.03',S:'≤0.015',P:'≤0.015'}, tensile:{Rm:'410-550'}, remarks:'低S/P' },
  { brand:'H08MnA', model:'H08MnA', fNo:'F-6', aNo:'A-1', category:'碳钢埋弧焊丝', standard:'GB/T 5293-2018', type:'实芯焊丝', depositSize:'Φ2.5/3.2/4.0/5.0', composition:{C:'≤0.10',Mn:'0.80-1.10',Si:'≤0.07',S:'≤0.030',P:'≤0.030'}, tensile:{Rm:'410-550'}, remarks:'配焊剂SJ431常用' },
  { brand:'H10Mn2', model:'H10Mn2', fNo:'F-6', aNo:'A-1', category:'碳钢埋弧焊丝', standard:'GB/T 5293-2018', type:'实芯焊丝', depositSize:'Φ3.2/4.0/5.0', composition:{C:'≤0.12',Mn:'1.50-1.90',Si:'≤0.07',S:'≤0.035',P:'≤0.035'}, tensile:{Rm:'480-640'}, remarks:'配焊剂SJ101常用' },
  { brand:'H08MnMoA', model:'H08MnMoA', fNo:'F-6', aNo:'A-2', category:'低合金钢埋弧焊丝', standard:'GB/T 12470', type:'实芯焊丝', depositSize:'Φ3.2/4.0', composition:{C:'0.06-0.10',Mn:'1.20-1.70',Mo:'0.30-0.50',Si:'≤0.15',S:'≤0.025',P:'≤0.030'}, tensile:{Rm:'550-700'}, remarks:'Q345R用' },
  { brand:'H08CrMoA', model:'H08CrMoA', fNo:'F-6', aNo:'A-2', category:'低合金耐热钢埋弧焊丝', standard:'GB/T 12470', type:'实芯焊丝', depositSize:'Φ3.2/4.0', composition:{C:'0.06-0.10',Mn:'0.40-0.70',Cr:'0.80-1.10',Mo:'0.40-0.60',Si:'≤0.15'}, tensile:{Rm:'540-690'}, remarks:'15CrMo用' },
  { brand:'H13CrMoA', model:'H13CrMoA', fNo:'F-6', aNo:'A-2', category:'低合金耐热钢埋弧焊丝', standard:'GB/T 12470', type:'实芯焊丝', depositSize:'Φ3.2/4.0', composition:{C:'0.11-0.16',Mn:'0.40-0.70',Cr:'0.80-1.10',Mo:'0.40-0.60',Si:'≤0.15'}, tensile:{Rm:'590-740'} },
  { brand:'H08CrMoVA', model:'H08CrMoVA', fNo:'F-6', aNo:'A-2', category:'低合金耐热钢埋弧焊丝', standard:'GB/T 12470', type:'实芯焊丝', depositSize:'Φ3.2/4.0', composition:{C:'0.06-0.10',Mn:'0.40-0.70',Cr:'1.00-1.30',Mo:'0.50-0.70',V:'0.20-0.35',Si:'≤0.15'}, tensile:{Rm:'550-700'}, remarks:'12Cr1MoV用' },

  // ============ 焊剂 GB/T 5293 / GB/T 36037 ============
  { brand:'SJ431', model:'SJ431', fNo:'F-1', aNo:'A-1', category:'埋弧焊焊剂', standard:'GB/T 5293-2018', type:'硅锰型', depositSize:'粒度10-60目', composition:{'MnO+SiO2':'≥50','CaO+MgO':'≤15',FeO:'≤1.5'}, remarks:'熔炼焊剂,通用' },
  { brand:'SJ101', model:'SJ101', fNo:'F-1', aNo:'A-2', category:'埋弧焊焊剂', standard:'GB/T 36037-2018', type:'氟碱型', depositSize:'粒度10-60目', composition:{'CaO+MgO+SiO2+Al2O3':'≥50',CaF2:'≥15',FeO:'≤1.0'}, remarks:'烧结焊剂,碱性' },
  { brand:'SJ301', model:'SJ301', fNo:'F-1', aNo:'A-1', category:'埋弧焊焊剂', standard:'GB/T 36037-2018', type:'硅钙型', depositSize:'粒度10-60目', composition:{'SiO2+MnO+CaF2+MgO':'≥50',Al2O3:'≤20'}, remarks:'烧结焊剂,中性' },
  { brand:'HJ431', model:'HJ431', fNo:'F-1', aNo:'A-1', category:'埋弧焊焊剂', standard:'GB/T 5293-2018', type:'熔炼焊剂', depositSize:'粒度10-60目', composition:{MnO:'34-38',SiO2:'40-44',CaF2:'3-7',MgO:'5-8'}, remarks:'传统熔炼焊剂' }
];
