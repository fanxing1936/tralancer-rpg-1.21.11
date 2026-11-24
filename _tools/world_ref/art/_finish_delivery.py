from pathlib import Path
from collections import Counter
import hashlib
import json
import zipfile
from PIL import Image
from export_native import validate

HERE=Path(__file__).resolve().parent
specs=json.loads((HERE/'generation_manifest.json').read_text(encoding='utf-8'))
stats=json.loads((HERE/'validation.json').read_text(encoding='utf-8'))
by_id={s['id']:s for s in specs}
by_stat={s['id']:s for s in stats}
order=['elite_badge','sin_shard','blueprint_fragment','blueprint_epic','blueprint_legend','star_fragment','wind_essence','abyss_tear','molten_core','mountain_heart','temple_bronze','grave_soil','title_gate','title_ledger','title_waverer','title_grandmaster','title_meteor','title_merchant']
original=HERE/'dungeons/T_Paper_Graph_02.png'
source=HERE/'_inspection_badges/assets/Dungeons/Content/Decor/Prefabs/_Lab/Paper/T_Paper_Graph_02.png'
assert original.read_bytes()==source.read_bytes(), 'Original source must remain byte-identical'
paper=Image.open(original).convert('RGBA')
assert paper.size==(32,32)
assert set(paper.getchannel('A').get_flattened_data())=={0,255}
paper_colors=len({p[:3] for p in paper.get_flattened_data() if p[3]})
paper_hash=hashlib.sha256(original.read_bytes()).hexdigest()
package_path='Dungeons/Content/Decor/Prefabs/_Lab/Paper/T_Paper_Graph_02.uasset'
entries=[]
rows=[]
for id in order:
    if id=='blueprint_fragment':
        entry=dict(id=id,file='dungeons/T_Paper_Graph_02.png',provenance='original_game_texture',package_path=package_path,size=[32,32],colors=paper_colors,alpha=[0,255],sha256=paper_hash)
        rows.append(f'| `{id}` 图纸碎片 | 原包导出，未绘制 | `dungeons/T_Paper_Graph_02.png` | 32×32 / {paper_colors} |')
    else:
        s=by_id[id]
        check=validate(s)
        assert check['sha256']==by_stat[id]['sha256']
        entry=dict(id=id,file=id+'.png',provenance='image_gen_then_native_export',attempts=s['attempts'],adopted_attempt=s['adopted_attempt'],**{k:check[k] for k in ['size','colors','alpha','sha256']})
        rows.append(f"| `{id}` {s['name']} | 绘制{s['attempts']}次，采用第{s['adopted_attempt']}张 | `{id}.png` | 16×16 / {check['colors']} |")
    entries.append(entry)
assert len(entries)==18 and len(specs)==17
(HERE/'DELIVERY-MANIFEST.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')

report='''# 世界掉落与锻造图标交付

日期：2026-11-23。依据同目录上级的 ART-BRIEF.md；本批只完成找图、绘图、像素导出和交付文件，未改物品定义、模型、字体映射或其他项目代码。

## 交付结果

18项：17张新绘的16×16透明PNG，以及1张保留原尺寸的地下城原包图纸素材。新绘材料为5–8色，六张称号各3色；全部生产PNG的Alpha仅0或255。总览见 PREVIEW.png，逐文件路径和SHA-256见 DELIVERY-MANIFEST.json。

原包素材优先：检索本机完整包索引的相关名称，并对候选导出/读取PNG进行目视。多数候选是模型表面展开图、场景纹理或半透明特效，不能直接代替简报要求的独立物品轮廓。采用一张原版纸张；其他17项新绘。没有把“未找到直接可用项”写成“游戏所有资源绝对不存在”。逐项检索依据见 item_source_search.md、element_source_search.md、title_source_search.md。

## 每项来源与采用版本

新绘使用内置 image_gen。绘制次数只统计生图调用，不把缩放、归并色板、透明度清理或选择采样位置算成新稿。

| ID / 名称 | 来源及次数 | 交付文件 | 尺寸 / 可见RGB色数 |
| --- | --- | --- | --- |
'''+ '\n'.join(rows)+f'''

## 原版图纸的准确来源

- 原包路径：`{package_path}`。
- 游戏包位置：`D:/XboxGames/Minecraft Dungeons/Content/Dungeons/Content/Paks`。
- 导出文件：`dungeons/T_Paper_Graph_02.png`，原生32×32，{paper_colors}色，Alpha 0/255。
- SHA-256：`{paper_hash}`。
- 已与本次候选导出的PNG逐字节核对一致，没有裁切、缩放、改色或透明度处理。

这张原图是带旧线稿的破边羊皮纸，供 `blueprint_fragment` 使用；它仍是完整原版纸张素材，尚不是裁成一角的16×16碎片。遵循简报“原图不是16×16的，导出原尺寸，我们来裁切和补边”，本批保留32×32交给后续适配，不另伪造一个16×16原版文件。

## 新绘与像素处理

17项共进行了20次生成。`sin_shard`、`blueprint_epic`、`blueprint_legend`各重画一次并采用第二张：罪印改为被断边截开的暗刻痕；两张图纸加宽纸面，用直刃、横护手和短柄表达武器线稿，分别保留紫绳与金绳/金边。其余14项采用第一张。

生成器底稿为1254×1254，不能直接当作16×16资源交付。按用户已经批准的文件级像素处理，使用 `export_native.py`：裁出有效Alpha区域、等比例最近邻取样至最大边14像素、居中放进16×16画布、归并到每张指定色板、Alpha以128为阈值变为0或255。无双线性或平滑缩放。

星晶、铜锭、史诗图纸和天平使用明确记录的采样位移，保留白色星点、十字压印、紫绳及天平盘底。账本色板收敛为深炭灰紫的黑皮明暗与纸页色。全部参数、每次提示词、生成原文件路径、采用次数在 `generation_manifest.json`；20张原始生成图保存在 `_generation/`，原生成文件亦保留原位。

像素整理只处理新绘底稿；原版纸张从未进入导出脚本的缩放分支。预览中的放大图只供查看，生产文件保持其上表尺寸。

## 验证

- 新绘17张均16×16、RGBA，Alpha集合恰为0和255；可见色全部来自各自受控色板；无可见纯黑像素。
- 罪印碎片每个可见像素均R=G=B，可供后续染色。
- 六张称号各3色。已查看16像素原图、放大图和8像素缩小预览；天平在8像素会合并托盘内部空隙，保留的是双盘、横梁与中央柱的整体意象。
- 已目视核对明暗方向、独立轮廓、主材料与关键符号；程序统计和PNG哈希见 `validation.json`。预览背景、中文名称不在生产PNG内。
- 未做游戏内字体注册、物品模型替换或实际客户端显示测试；这些不属于本次美术简报。

## 文件说明

- `world_art.zip`：18项生产图、总览、报告、三份原图检索记录、生成记录、验证数据、导出脚本及20张生成底稿。
- `PREVIEW.png`：6列×3行总览，包含原尺寸/2倍查看，称号另外显示8像素检查图。
- `DELIVERY-MANIFEST.json`：18项ID到生产文件的映射，原版纸张不在根目录伪装成新绘文件。
- `_inspection_*`：本机候选和采样检查资料，不属于交付图，不收入ZIP。

重新导出新绘图：在装有Pillow的Python环境执行 `python export_native.py`。脚本从随包的 `_generation/` 读取底稿，可重复生成17张PNG、validation.json和PREVIEW.png，不依赖桌面软件。
'''
(HERE/'REPORT.md').write_text(report,encoding='utf-8')
files=[e['file'] for e in entries]+['PREVIEW.png','REPORT.md','DELIVERY-MANIFEST.json','generation_manifest.json','validation.json','export_native.py','item_source_search.md','element_source_search.md','title_source_search.md']
files+=sorted({h['source'] for s in specs for h in s['generation_history']})
with zipfile.ZipFile(HERE/'world_art.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
    for name in files:
        archive.write(HERE/name,name)
with zipfile.ZipFile(HERE/'world_art.zip') as archive:
    assert archive.testzip() is None
    assert all(e['file'] in archive.namelist() for e in entries)
print(json.dumps(dict(production_images=len(entries),new_native_16=len(specs),original_32=1,generated_attempts=sum(s['attempts'] for s in specs),zip_files=len(files),zip_bytes=(HERE/'world_art.zip').stat().st_size,zip_crc='PASS',original_unchanged=True),ensure_ascii=False))
