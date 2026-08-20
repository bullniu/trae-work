/**
 * 焊接工艺评定知识库 - 母材库
 * 依据:GB/T 700、GB/T 713 系列、GB/T 5310、GB/T 9948、GB/T 1220、GB/T 4238、GB/T 14976、GB/T 9711 等
 * 字段说明:
 *   grade        牌号
 *   category     类别号(NB/T 47014 P-No.)
 *   groupNo      组别号(NB/T 47014 Group No.)
 *   standard     所属标准号
 *   productForm  产品形态(板/管/棒/锻)
 *   supplyStatus 供货状态
 *   heatTreatment 热处理状态
 *   buttThicknessRange  对接焊缝适用母材厚度范围(标准规定)
 *   composition  化学成分(%)
 *   tensile      力学性能
 *   remarks      说明
 */
window.KB_BASE_METALS = [
  // ============ Fe-1 碳钢(类别号1,组别1) ============
  { grade:'Q195', category:'Fe-1', groupNo:'1', standard:'GB/T 700', productForm:'板/棒', supplyStatus:'热轧', heatTreatment:'轧制态', composition:{C:'0.06-0.12',Si:'≤0.30',Mn:'0.25-0.50',P:'≤0.045',S:'≤0.045'}, tensile:{Rm:'315-430',Rel:'195'}, remarks:'碳素结构钢' },
  { grade:'Q215', category:'Fe-1', groupNo:'1', standard:'GB/T 700', productForm:'板/棒', supplyStatus:'热轧', heatTreatment:'轧制态', composition:{C:'0.09-0.15',Si:'≤0.30',Mn:'0.25-0.55',P:'≤0.045',S:'≤0.045'}, tensile:{Rm:'335-450',Rel:'215'}, remarks:'碳素结构钢' },
  { grade:'Q235A', category:'Fe-1', groupNo:'1', standard:'GB/T 700', productForm:'板/棒', supplyStatus:'热轧', heatTreatment:'轧制态', composition:{C:'0.14-0.22',Si:'≤0.30',Mn:'0.30-0.65',P:'≤0.045',S:'≤0.045'}, tensile:{Rm:'370-500',Rel:'235'}, remarks:'碳素结构钢,常用' },
  { grade:'Q235B', category:'Fe-1', groupNo:'1', standard:'GB/T 700', productForm:'板/棒', supplyStatus:'热轧', heatTreatment:'轧制态', composition:{C:'0.14-0.22',Si:'≤0.35',Mn:'0.30-0.70',P:'≤0.045',S:'≤0.045'}, tensile:{Rm:'370-500',Rel:'235'}, remarks:'碳素结构钢,常用' },
  { grade:'Q235C', category:'Fe-1', groupNo:'1', standard:'GB/T 700', productForm:'板/棒', supplyStatus:'热轧', heatTreatment:'轧制态', composition:{C:'≤0.20',Si:'≤0.35',Mn:'0.30-0.70',P:'≤0.040',S:'≤0.040'}, tensile:{Rm:'370-500',Rel:'235'}, remarks:'碳素结构钢' },
  { grade:'Q235D', category:'Fe-1', groupNo:'1', standard:'GB/T 700', productForm:'板/棒', supplyStatus:'热轧', heatTreatment:'轧制态', composition:{C:'≤0.17',Si:'≤0.35',Mn:'0.30-0.70',P:'≤0.035',S:'≤0.035'}, tensile:{Rm:'370-500',Rel:'235'}, remarks:'碳素结构钢' },
  { grade:'Q255', category:'Fe-1', groupNo:'1', standard:'GB/T 700', productForm:'板/棒', supplyStatus:'热轧', heatTreatment:'轧制态', composition:{C:'0.18-0.28',Si:'≤0.30',Mn:'0.40-0.70',P:'≤0.045',S:'≤0.045'}, tensile:{Rm:'410-550',Rel:'255'} },
  { grade:'Q275', category:'Fe-1', groupNo:'1', standard:'GB/T 700', productForm:'板/棒', supplyStatus:'热轧', heatTreatment:'轧制态', composition:{C:'0.20-0.28',Si:'≤0.35',Mn:'0.50-0.80',P:'≤0.045',S:'≤0.045'}, tensile:{Rm:'410-540',Rel:'275'} },
  { grade:'Q245R', category:'Fe-1', groupNo:'1', standard:'GB/T 713.2', productForm:'板', supplyStatus:'热轧/控轧/正火', heatTreatment:'轧制或正火', buttThicknessRange:'3-25', composition:{C:'≤0.20',Si:'0.15-0.30',Mn:'0.50-1.00',P:'≤0.025',S:'≤0.015',Al:'≥0.020'}, tensile:{Rm:'400-520',Rel:'235-245'}, remarks:'锅炉压力容器用钢板' },
  { grade:'Q345R', category:'Fe-1', groupNo:'1', standard:'GB/T 713.2', productForm:'板', supplyStatus:'热轧/控轧/正火', heatTreatment:'轧制或正火', buttThicknessRange:'3-25', composition:{C:'≤0.20',Si:'≤0.55',Mn:'1.10-1.70',P:'≤0.025',S:'≤0.015',Al:'≥0.020'}, tensile:{Rm:'500-640',Rel:'325-345'}, remarks:'压力容器用,常用' },
  { grade:'10', category:'Fe-1', groupNo:'1', standard:'GB/T 699', productForm:'棒/锻', supplyStatus:'热轧', heatTreatment:'正火', composition:{C:'0.07-0.13',Si:'0.17-0.37',Mn:'0.35-0.65',P:'≤0.035',S:'≤0.035'}, tensile:{Rm:'335',Rel:'205'}, remarks:'优质碳素结构钢' },
  { grade:'20', category:'Fe-1', groupNo:'1', standard:'GB/T 699', productForm:'棒/锻', supplyStatus:'热轧', heatTreatment:'正火', composition:{C:'0.17-0.23',Si:'0.17-0.37',Mn:'0.35-0.65',P:'≤0.035',S:'≤0.035'}, tensile:{Rm:'410',Rel:'245'}, remarks:'优质碳素结构钢,常用' },
  { grade:'25', category:'Fe-1', groupNo:'1', standard:'GB/T 699', productForm:'棒/锻', supplyStatus:'热轧', heatTreatment:'正火', composition:{C:'0.22-0.29',Si:'0.17-0.37',Mn:'0.50-0.80',P:'≤0.035',S:'≤0.035'}, tensile:{Rm:'450',Rel:'275'} },
  { grade:'35', category:'Fe-1', groupNo:'1', standard:'GB/T 699', productForm:'棒/锻', supplyStatus:'热轧', heatTreatment:'正火', composition:{C:'0.32-0.39',Si:'0.17-0.37',Mn:'0.50-0.80',P:'≤0.035',S:'≤0.035'}, tensile:{Rm:'530',Rel:'315'} },
  { grade:'45', category:'Fe-1', groupNo:'1', standard:'GB/T 699', productForm:'棒/锻', supplyStatus:'热轧', heatTreatment:'正火', composition:{C:'0.42-0.50',Si:'0.17-0.37',Mn:'0.50-0.80',P:'≤0.035',S:'≤0.035'}, tensile:{Rm:'600',Rel:'355'} },
  { grade:'20G', category:'Fe-1', groupNo:'1', standard:'GB/T 5310', productForm:'管', supplyStatus:'热轧/正火', heatTreatment:'正火', buttThicknessRange:'≤16', composition:{C:'0.17-0.23',Si:'0.17-0.37',Mn:'0.35-0.65',P:'≤0.025',S:'≤0.015'}, tensile:{Rm:'410-550',Rel:'245'}, remarks:'锅炉用无缝钢管' },
  { grade:'10钢(GB/T 9948)', category:'Fe-1', groupNo:'1', standard:'GB/T 9948-2025', productForm:'管', supplyStatus:'正火', heatTreatment:'正火', buttThicknessRange:'≤16', composition:{C:'0.07-0.13',Si:'0.17-0.37',Mn:'0.35-0.65',P:'≤0.030',S:'≤0.020'}, tensile:{Rm:'335-475',Rel:'205'}, remarks:'石油裂化用无缝钢管' },
  { grade:'20钢(GB/T 9948)', category:'Fe-1', groupNo:'1', standard:'GB/T 9948-2025', productForm:'管', supplyStatus:'正火', heatTreatment:'正火', buttThicknessRange:'≤16', composition:{C:'0.17-0.23',Si:'0.17-0.37',Mn:'0.35-0.65',P:'≤0.030',S:'≤0.020'}, tensile:{Rm:'410-550',Rel:'245'}, remarks:'石油裂化用无缝钢管' },
  { grade:'L175', category:'Fe-1', groupNo:'1', standard:'GB/T 9711-2017', productForm:'管', supplyStatus:'热轧', heatTreatment:'轧制态', composition:{C:'≤0.21',Mn:'≤0.60'}, tensile:{Rm:'≥359',Rel:'≥175'}, remarks:'石油天然气输送管' },
  { grade:'L210', category:'Fe-1', groupNo:'1', standard:'GB/T 9711-2017', productForm:'管', supplyStatus:'热轧', heatTreatment:'轧制态', composition:{C:'≤0.22',Mn:'≤0.90'}, tensile:{Rm:'≥335',Rel:'≥210'}, remarks:'石油天然气输送管' },
  { grade:'L245', category:'Fe-1', groupNo:'1', standard:'GB/T 9711-2017', productForm:'管', supplyStatus:'热轧', heatTreatment:'轧制态', composition:{C:'≤0.26',Mn:'≤1.15'}, tensile:{Rm:'≥415',Rel:'≥245'}, remarks:'石油天然气输送管,常用' },
  { grade:'L290', category:'Fe-1', groupNo:'1', standard:'GB/T 9711-2017', productForm:'管', supplyStatus:'热轧/控轧', heatTreatment:'轧制或控轧', composition:{C:'≤0.28',Mn:'≤1.25'}, tensile:{Rm:'≥415',Rel:'≥290'} },
  { grade:'L320', category:'Fe-1', groupNo:'1', standard:'GB/T 9711-2017', productForm:'管', supplyStatus:'热轧/控轧', heatTreatment:'轧制或控轧', composition:{C:'≤0.30',Mn:'≤1.35'}, tensile:{Rm:'≥435',Rel:'≥320'} },
  { grade:'L360', category:'Fe-1', groupNo:'1', standard:'GB/T 9711-2017', productForm:'管', supplyStatus:'热轧/控轧', heatTreatment:'轧制或控轧', composition:{C:'≤0.30',Mn:'≤1.40'}, tensile:{Rm:'≥460',Rel:'≥360'} },
  { grade:'L415', category:'Fe-1', groupNo:'2', standard:'GB/T 9711-2017', productForm:'管', supplyStatus:'控轧', heatTreatment:'控轧', composition:{C:'≤0.28',Mn:'≤1.65'}, tensile:{Rm:'≥520',Rel:'≥415'} },

  // ============ Fe-2 低合金钢(类别号2) ============
  { grade:'Q355', category:'Fe-2', groupNo:'1', standard:'GB/T 1591', productForm:'板/棒', supplyStatus:'热轧/控轧/正火', heatTreatment:'轧制或正火', buttThicknessRange:'3-25', composition:{C:'≤0.20',Si:'≤0.55',Mn:'1.00-1.60',P:'≤0.035',S:'≤0.035',V:'0.02-0.15',Nb:'0.015-0.060',Ti:'0.02-0.20'}, tensile:{Rm:'470-630',Rel:'355'}, remarks:'低合金高强度结构钢' },
  { grade:'Q355B', category:'Fe-2', groupNo:'1', standard:'GB/T 1591', productForm:'板/棒', supplyStatus:'热轧/正火', heatTreatment:'轧制或正火', buttThicknessRange:'3-25', composition:{C:'≤0.20',Si:'≤0.55',Mn:'1.00-1.60',P:'≤0.035',S:'≤0.035'}, tensile:{Rm:'470-630',Rel:'355'}, remarks:'低合金高强度结构钢,常用' },
  { grade:'Q355C', category:'Fe-2', groupNo:'1', standard:'GB/T 1591', productForm:'板/棒', supplyStatus:'热轧/正火', heatTreatment:'轧制或正火', composition:{C:'≤0.20',Si:'≤0.55',Mn:'1.00-1.60',P:'≤0.030',S:'≤0.030'}, tensile:{Rm:'470-630',Rel:'355'} },
  { grade:'Q355D', category:'Fe-2', groupNo:'1', standard:'GB/T 1591', productForm:'板/棒', supplyStatus:'热轧/正火', heatTreatment:'轧制或正火', composition:{C:'≤0.18',Si:'≤0.55',Mn:'1.00-1.60',P:'≤0.025',S:'≤0.020'}, tensile:{Rm:'470-630',Rel:'355'} },
  { grade:'Q370R', category:'Fe-2', groupNo:'1', standard:'GB/T 713.5', productForm:'板', supplyStatus:'正火', heatTreatment:'正火', buttThicknessRange:'10-25', composition:{C:'≤0.18',Si:'0.15-0.50',Mn:'1.20-1.60',P:'≤0.025',S:'≤0.015',Nb:'0.005-0.050'}, tensile:{Rm:'520-630',Rel:'370'} },
  { grade:'Q390', category:'Fe-2', groupNo:'1', standard:'GB/T 1591', productForm:'板/棒', supplyStatus:'热轧/正火', heatTreatment:'轧制或正火', composition:{C:'≤0.20',Si:'≤0.55',Mn:'1.00-1.60',P:'≤0.035',S:'≤0.035',V:'0.02-0.20',Nb:'0.015-0.060'}, tensile:{Rm:'490-650',Rel:'390'} },
  { grade:'Q420', category:'Fe-2', groupNo:'2', standard:'GB/T 1591', productForm:'板/棒', supplyStatus:'热轧/正火', heatTreatment:'轧制或正火', composition:{C:'≤0.20',Si:'≤0.55',Mn:'1.00-1.70',P:'≤0.035',S:'≤0.035',V:'0.02-0.20',Nb:'0.015-0.060',Ti:'0.02-0.20'}, tensile:{Rm:'520-680',Rel:'420'} },
  { grade:'Q460', category:'Fe-2', groupNo:'2', standard:'GB/T 1591', productForm:'板/棒', supplyStatus:'热轧/正火', heatTreatment:'轧制或正火', composition:{C:'≤0.20',Si:'≤0.55',Mn:'1.00-1.80',P:'≤0.035',S:'≤0.035',V:'0.02-0.20',Nb:'0.015-0.060',Ti:'0.02-0.20'}, tensile:{Rm:'550-720',Rel:'460'} },

  // ============ Fe-3 低合金耐热钢(类别号3) ============
  { grade:'12CrMoG', category:'Fe-3', groupNo:'1', standard:'GB/T 5310', productForm:'管', supplyStatus:'正火+回火', heatTreatment:'正火+回火', buttThicknessRange:'≤16', composition:{C:'0.08-0.15',Si:'0.17-0.37',Mn:'0.40-0.70',Cr:'0.40-0.70',Mo:'0.40-0.55',P:'≤0.025',S:'≤0.015'}, tensile:{Rm:'410-580',Rel:'225'} },
  { grade:'15CrMoG', category:'Fe-3', groupNo:'1', standard:'GB/T 5310', productForm:'管', supplyStatus:'正火+回火', heatTreatment:'正火+回火', buttThicknessRange:'≤16', composition:{C:'0.12-0.18',Si:'0.17-0.37',Mn:'0.40-0.70',Cr:'0.80-1.10',Mo:'0.45-0.55',P:'≤0.025',S:'≤0.015'}, tensile:{Rm:'440-640',Rel:'235'}, remarks:'常用耐热钢' },
  { grade:'12Cr1MoVG', category:'Fe-3', groupNo:'2', standard:'GB/T 5310', productForm:'管', supplyStatus:'正火+回火', heatTreatment:'正火+回火', buttThicknessRange:'≤16', composition:{C:'0.08-0.15',Si:'0.17-0.37',Mn:'0.40-0.70',Cr:'0.90-1.20',Mo:'0.25-0.35',V:'0.15-0.30',P:'≤0.025',S:'≤0.015'}, tensile:{Rm:'470-640',Rel:'255'} },
  { grade:'15Cr1Mo1G', category:'Fe-3', groupNo:'2', standard:'GB/T 5310', productForm:'管', supplyStatus:'正火+回火', heatTreatment:'正火+回火', buttThicknessRange:'≤16', composition:{C:'0.12-0.18',Mn:'0.40-0.70',Cr:'0.80-1.20',Mo:'0.90-1.10'}, tensile:{Rm:'470-640',Rel:'255'} },
  { grade:'12Cr2MoG', category:'Fe-3', groupNo:'2', standard:'GB/T 5310', productForm:'管', supplyStatus:'正火+回火', heatTreatment:'正火+回火', buttThicknessRange:'≤16', composition:{C:'0.08-0.15',Si:'≤0.50',Mn:'0.40-0.70',Cr:'2.00-2.50',Mo:'0.90-1.20',P:'≤0.025',S:'≤0.015'}, tensile:{Rm:'450-600',Rel:'280'} },

  // ============ Fe-4 低合金耐热钢(高Cr) ============
  { grade:'10Cr9Mo1VNbN', category:'Fe-4', groupNo:'1', standard:'GB/T 5310', productForm:'管', supplyStatus:'正火+回火', heatTreatment:'正火+回火', buttThicknessRange:'≤16', composition:{C:'0.08-0.12',Cr:'8.00-9.50',Mo:'0.85-1.05',V:'0.18-0.25',Nb:'0.06-0.10',N:'0.03-0.07'}, tensile:{Rm:'≥585',Rel:'≥415'}, remarks:'T91/P91型' },

  // ============ Fe-5A 马氏体不锈钢 ============
  { grade:'06Cr13', category:'Fe-5A', groupNo:'1', standard:'GB/T 1220', productForm:'板/棒', supplyStatus:'退火', heatTreatment:'退火', composition:{C:'≤0.08',Cr:'11.50-13.50',Si:'≤1.00',Mn:'≤1.00',P:'≤0.040',S:'≤0.030'}, tensile:{Rm:'≥410',Rel:'≥205'}, remarks:'马氏体型' },
  { grade:'12Cr13', category:'Fe-5A', groupNo:'1', standard:'GB/T 1220', productForm:'板/棒', supplyStatus:'退火/淬火+回火', heatTreatment:'退火', composition:{C:'0.08-0.15',Cr:'11.50-13.50',Si:'≤1.00',Mn:'≤1.00',P:'≤0.040',S:'≤0.030'}, tensile:{Rm:'≥540',Rel:'≥345'} },
  { grade:'20Cr13', category:'Fe-5A', groupNo:'1', standard:'GB/T 1220', productForm:'板/棒', supplyStatus:'淬火+回火', heatTreatment:'淬火+回火', composition:{C:'0.16-0.25',Cr:'12.00-14.00',Si:'≤1.00',Mn:'≤1.00',P:'≤0.040',S:'≤0.030'}, tensile:{Rm:'≥640',Rel:'≥440'} },

  // ============ Fe-6 沉淀硬化不锈钢(简化) ============
  { grade:'06Cr17Ni7Al', category:'Fe-6', groupNo:'1', standard:'GB/T 1220', productForm:'板/棒', supplyStatus:'固溶', heatTreatment:'固溶+时效', composition:{C:'≤0.09',Cr:'16.00-18.00',Ni:'6.50-7.75',Al:'0.75-1.50'}, tensile:{Rm:'≥725'}, remarks:'17-7PH' },

  // ============ Fe-7A 铁素体不锈钢 ============
  { grade:'06Cr13Al', category:'Fe-7A', groupNo:'1', standard:'GB/T 4238', productForm:'板', supplyStatus:'退火', heatTreatment:'退火', composition:{C:'≤0.08',Cr:'11.50-14.50',Al:'0.10-0.30',Si:'≤1.00',Mn:'≤1.00',P:'≤0.040',S:'≤0.030'}, tensile:{Rm:'≥415',Rel:'≥205'}, remarks:'铁素体型' },
  { grade:'022Cr11', category:'Fe-7A', groupNo:'1', standard:'GB/T 4238', productForm:'板', supplyStatus:'退火', heatTreatment:'退火', composition:{C:'≤0.030',Cr:'10.50-11.70',Si:'≤1.00',Mn:'≤1.00',P:'≤0.040',S:'≤0.030'}, tensile:{Rm:'≥410'}, remarks:'409型' },
  { grade:'022Cr12', category:'Fe-7A', groupNo:'1', standard:'GB/T 4238', productForm:'板', supplyStatus:'退火', heatTreatment:'退火', composition:{C:'≤0.030',Cr:'11.00-13.50',Ni:'≤0.60',Si:'≤1.00',Mn:'≤1.00',P:'≤0.040',S:'≤0.030'}, tensile:{Rm:'≥360',Rel:'≥195'}, remarks:'410L型' },
  { grade:'022Cr12Ni', category:'Fe-7A', groupNo:'2', standard:'GB/T 4238', productForm:'板', supplyStatus:'退火', heatTreatment:'退火', composition:{C:'≤0.030',Cr:'11.00-13.00',Ni:'0.30-1.00',Si:'≤1.00',Mn:'≤1.50',P:'≤0.040',S:'≤0.030'}, tensile:{Rm:'≥410'} },
  { grade:'06Cr13', category:'Fe-7A', groupNo:'1', standard:'GB/T 4238', productForm:'板', supplyStatus:'退火', heatTreatment:'退火', composition:{C:'≤0.08',Cr:'11.50-13.50',Si:'≤1.00',Mn:'≤1.00',P:'≤0.040',S:'≤0.030'}, tensile:{Rm:'≥415'}, remarks:'410S型' },
  { grade:'06Cr11Ti', category:'Fe-7A', groupNo:'1', standard:'GB/T 4238', productForm:'板', supplyStatus:'退火', heatTreatment:'退火', composition:{C:'≤0.08',Cr:'10.50-11.75',Ti:'6×C-0.75',Si:'≤1.00',Mn:'≤1.00'}, tensile:{Rm:'≥415'}, remarks:'409Ti型' },

  // ============ Fe-8 奥氏体不锈钢 ============
  { grade:'06Cr19Ni10', category:'Fe-8', groupNo:'1', standard:'GB/T 14976-2025', productForm:'管', supplyStatus:'固溶', heatTreatment:'固溶', buttThicknessRange:'≤8', composition:{C:'≤0.08',Si:'≤1.00',Mn:'≤2.00',P:'≤0.035',S:'≤0.030',Cr:'18.00-20.00',Ni:'8.00-11.00'}, tensile:{Rm:'≥520',Rel:'≥205'}, remarks:'304型' },
  { grade:'022Cr19Ni10', category:'Fe-8', groupNo:'1', standard:'GB/T 14976-2025', productForm:'管', supplyStatus:'固溶', heatTreatment:'固溶', buttThicknessRange:'≤8', composition:{C:'≤0.030',Si:'≤1.00',Mn:'≤2.00',P:'≤0.035',S:'≤0.030',Cr:'18.00-20.00',Ni:'8.00-12.00'}, tensile:{Rm:'≥520',Rel:'≥205'}, remarks:'304L型' },
  { grade:'06Cr17Ni12Mo2', category:'Fe-8', groupNo:'1', standard:'GB/T 14976-2025', productForm:'管', supplyStatus:'固溶', heatTreatment:'固溶', buttThicknessRange:'≤8', composition:{C:'≤0.08',Si:'≤1.00',Mn:'≤2.00',P:'≤0.035',S:'≤0.030',Cr:'16.00-18.00',Ni:'10.00-14.00',Mo:'2.00-3.00'}, tensile:{Rm:'≥530',Rel:'≥205'}, remarks:'316型' },
  { grade:'022Cr17Ni12Mo2', category:'Fe-8', groupNo:'1', standard:'GB/T 14976-2025', productForm:'管', supplyStatus:'固溶', heatTreatment:'固溶', buttThicknessRange:'≤8', composition:{C:'≤0.030',Si:'≤1.00',Mn:'≤2.00',P:'≤0.035',S:'≤0.030',Cr:'16.00-18.00',Ni:'10.00-14.00',Mo:'2.00-3.00'}, tensile:{Rm:'≥520',Rel:'≥205'}, remarks:'316L型' },
  { grade:'06Cr18Ni11Ti', category:'Fe-8', groupNo:'1', standard:'GB/T 14976-2025', productForm:'管', supplyStatus:'固溶', heatTreatment:'固溶', buttThicknessRange:'≤8', composition:{C:'≤0.08',Si:'≤1.00',Mn:'≤2.00',P:'≤0.035',S:'≤0.030',Cr:'17.00-19.00',Ni:'9.00-12.00',Ti:'5×C-0.70'}, tensile:{Rm:'≥520',Rel:'≥205'}, remarks:'321型' },
  { grade:'06Cr18Ni11Nb', category:'Fe-8', groupNo:'1', standard:'GB/T 14976-2025', productForm:'管', supplyStatus:'固溶', heatTreatment:'固溶', buttThicknessRange:'≤8', composition:{C:'≤0.08',Si:'≤1.00',Mn:'≤2.00',P:'≤0.035',S:'≤0.030',Cr:'17.00-19.00',Ni:'9.00-13.00',Nb:'10×C-1.00'}, tensile:{Rm:'≥520',Rel:'≥205'}, remarks:'347型' },
  { grade:'06Cr25Ni20', category:'Fe-8', groupNo:'2', standard:'GB/T 14976-2025', productForm:'管', supplyStatus:'固溶', heatTreatment:'固溶', buttThicknessRange:'≤8', composition:{C:'≤0.08',Si:'≤1.50',Mn:'≤2.00',P:'≤0.035',S:'≤0.030',Cr:'24.00-26.00',Ni:'19.00-22.00'}, tensile:{Rm:'≥520',Rel:'≥205'}, remarks:'310型' },
  { grade:'16Cr25Ni20Si2', category:'Fe-8', groupNo:'2', standard:'GB/T 14976-2025', productForm:'管', supplyStatus:'固溶', heatTreatment:'固溶', buttThicknessRange:'≤8', composition:{C:'≤0.20',Si:'1.50-2.50',Mn:'≤1.50',P:'≤0.035',S:'≤0.030',Cr:'24.00-27.00',Ni:'18.00-21.00'}, tensile:{Rm:'≥590'}, remarks:'310s型' },

  // ============ Fe-9A/9B/10H/10I 镍基合金(简化) ============
  { grade:'NS312', category:'Fe-10H', groupNo:'1', standard:'GB/T 15011', productForm:'板/管/棒', supplyStatus:'固溶', heatTreatment:'固溶', buttThicknessRange:'≤8', composition:{C:'≤0.15',Cr:'14.00-17.00',Ni:'≥72',Fe:'6.00-10.00',Mn:'≤1.00',S:'≤0.015'}, tensile:{Rm:'≥550',Rel:'≥240'}, remarks:'Inconel 600' },
  { grade:'NS334', category:'Fe-10H', groupNo:'1', standard:'GB/T 15011', productForm:'板/管/棒', supplyStatus:'固溶', heatTreatment:'固溶', buttThicknessRange:'≤8', composition:{C:'≤0.02',Cr:'14.50-16.50',Mo:'15.00-17.00',W:'3.00-4.50',Ni:'余量',Fe:'4.00-7.00',Co:'≤2.5'}, tensile:{Rm:'≥690'}, remarks:'Hastelloy C-276' },
  { grade:'NS336', category:'Fe-10H', groupNo:'1', standard:'GB/T 15011', productForm:'板/管/棒', supplyStatus:'固溶', heatTreatment:'固溶', buttThicknessRange:'≤8', composition:{C:'≤0.10',Cr:'19.00-23.00',Mo:'7.00-13.00',Nb:'3.00-4.15',Ni:'余量',Fe:'≤5.0'}, tensile:{Rm:'≥690'}, remarks:'Inconel 625' }
];
