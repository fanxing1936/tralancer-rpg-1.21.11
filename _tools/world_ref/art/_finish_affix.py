from pathlib import Path
import json
import hashlib
import zipfile
from PIL import Image
from export_native import validate

HERE=Path(__file__).resolve().parent
specs=json.loads((HERE/'affix_generation_manifest.json').read_text(encoding='utf-8'))
stats={r['id']:r for r in json.loads((HERE/'affix_validation.json').read_text(encoding='utf-8'))}
prior=json.loads((HERE/'_affix_work/prior_delivery_manifest.json').read_text(encoding='utf-8'))
for p in prior:
    assert hashlib.sha256((HERE/p['file']).read_bytes()).hexdigest()==p['sha256'], 'Prior art changed: '+p['id']
entries=[]
table=[]
for s in specs:
    check=validate(s)
    assert check['sha256']==stats[s['id']]['sha256']
    entries.append(dict(id=s['id'],file=s['id']+'.png',provenance='image_gen_then_native_export',attempts=s['attempts'],adopted_attempt=s['adopted_attempt'],main_color=s['main'],**{k:check[k] for k in ['size','colors','alpha','sha256']}))
    table.append(f"| `{s['id']}.png` | {s['name']} | `{s['main']}` | 内置image_gen绘制{s['attempts']}次，采用第{s['adopted_attempt']}张 | 16×16 / {check['colors']}色 |")
refs=[]
for name,folder in [('T_IceSymbol','Effects/Materials/Ice'),('T_SkullSoul','Effects/Materials/Skull'),('T_ShadowSkull','Effects/Materials/Skull')]:
    p=HERE/'dungeons'/(name+'.png')
    src=HERE/'_inspection_affix_b/assets/Dungeons/Content'/folder/(name+'.png')
    assert p.read_bytes()==src.read_bytes()
    refs.append(dict(file='dungeons/'+name+'.png',purpose='reference_only_not_production_affix',original_package_path='Dungeons/Content/'+folder+'/'+name+'.uasset',size=list(Image.open(p).size),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(HERE/'affix_DELIVERY-MANIFEST.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'affix_REFERENCE-MANIFEST.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'DELIVERY-MANIFEST.json').write_text(json.dumps(prior+entries,ensure_ascii=False,indent=2),encoding='utf-8')
attempts=sum(s['attempts'] for s in specs)
section='''

---

## 追加：精英词缀图标（2026-11-23）

完成与复核日期：2026-11-24。

已按更新后的ART-BRIEF.md追加11张精英怪名牌词缀图标，全部为16×16透明PNG，各3色，Alpha仅0或255，并包含指定Hex主色。此前18项生产图逐文件SHA-256核对未变化。累计交付29项生产图：28张16×16新绘图和1张保留32×32的原版图纸。

### 来源与尝试次数

先在本机原版包中查找并实际查看候选。附魔卡面常见256×256、复杂背景和多级透明；其他候选在主色、轮廓或主体上不符。原版小雪花与单骷髅仅作参考部件保留，未补边、改色或缩放：雪花为6×6白色单色，单骷髅为7×7白色单色，三枚原宽无法横排进16像素。本批11张最终字形因此新绘，详细候选包路径与尺寸见affix_source_a.md、affix_source_b.md、affix_source_c.md。

| 文件 | 词缀 | 指定主色 | 来源、绘制与采用次数 | 交付规格 |
| --- | --- | --- | --- | --- |
'''+ '\n'.join(table)+f'''

本批共{attempts}次内置image_gen调用。原始生成图保存在 `_generation_affix/`；每次提示词、原生成文件路径、采用稿、三色调色板及采样偏移均记录于 `affix_generation_manifest.json`。原尺寸参考文件的精确路径、尺寸与哈希见 `affix_REFERENCE-MANIFEST.json`，三张参考不计入11张生产图。

### 像素整理与检查

使用用户此前批准的文件级像素处理：将新绘底稿裁至有效Alpha范围、最近邻采样至16×16画布、映射到指定三色调色板、清理为二值Alpha。通过取样位置选择保留形体和关键符号，不对原版参考图做缩放或改色。普通高分辨率生成稿不作为最终16×16资源。

吸血、召唤、罪染分别重画一次并采用第二稿，纠正了问号状獠牙、粘连的头部和与瞳孔融合的裂纹。召唤单独采用14×7有效区的非等比最近邻缩放与[-0.4,0.4]采样位移，保留三组成对眼窝和短颌；8px下相邻头部仍会连成紧凑组形，按三头整体意象辨认。其余图标采用等比例缩放。

- 11张实际PNG均16×16、RGBA、Alpha集合为0和255、3色；指定Hex主色真实存在于像素中，无可见纯黑或半透明边。
- 已检查16px原尺寸及8px最近邻缩小预览；总览中另放大8px结果供查看。静态字形检查不等于游戏客户端验证。
- 名牌图标仅表达各自轮廓和核心符号，圣印的亮感由金色和浅色块表示，最终PNG不带外发光或投影。
- 数据和哈希在 `affix_validation.json`；ID到文件映射在 `affix_DELIVERY-MANIFEST.json`。没有修改字体注册、名牌逻辑或其他项目代码。

### 新增交付文件

- `affix_*.png`：本次11张生产图。
- `AFFIX_PREVIEW.png`：新增11张总览，含16px、8px名牌示意、8px放大检查。
- `affix_icons.zip`：本次新增图及来源、验证、生成底稿、复现脚本。
- `world_art.zip`：已更新为全部29项生产图及两批记录；原版参考仍单列，不冒充词缀成品。
- `export_affix.py`：只复现这11张新图及其预览、验证文件；与随包 `export_native.py` 放在同一目录，装有Pillow后运行 `python export_affix.py`。
'''
prior_report=(HERE/'_affix_work/prior_report.md').read_text(encoding='utf-8')
(HERE/'REPORT.md').write_text(prior_report+section,encoding='utf-8')
common=['REPORT.md','affix_DELIVERY-MANIFEST.json','affix_REFERENCE-MANIFEST.json','AFFIX_PREVIEW.png','affix_generation_manifest.json','affix_validation.json','export_affix.py','export_native.py','affix_source_a.md','affix_source_b.md','affix_source_c.md']
affix_files=[e['file'] for e in entries]+common+[r['file'] for r in refs]+sorted({h['source'] for s in specs for h in s['generation_history']})
old_specs=json.loads((HERE/'generation_manifest.json').read_text(encoding='utf-8'))
old_files=[p['file'] for p in prior]+['PREVIEW.png','DELIVERY-MANIFEST.json','generation_manifest.json','validation.json','item_source_search.md','element_source_search.md','title_source_search.md']+sorted({h['source'] for s in old_specs for h in s['generation_history']})
for zip_name,files in [('affix_icons.zip',affix_files),('world_art.zip',affix_files+old_files)]:
    files=list(dict.fromkeys(files))
    tmp=HERE/(zip_name+'.tmp')
    with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name in files: archive.write(HERE/name,name)
    with zipfile.ZipFile(tmp) as archive:
        assert archive.testzip() is None
    tmp.replace(HERE/zip_name)
    print(zip_name,len(files),'files,', (HERE/zip_name).stat().st_size,'bytes, CRC PASS')
print('11 added; 29 total; prior 18 unchanged; 3 original references unchanged.')
