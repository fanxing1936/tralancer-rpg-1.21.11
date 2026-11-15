# 原始资产证据缺口：限定范围只读检查

日期：2026-11-07（Asia/Singapore）。目的：查找能补足 Root Rot Armor 背面、未知面及 UV 归属证据的 Minecraft Dungeons 原始游戏资产或有授权依据的原始网格来源。

**结果：在以下已查范围内未找到可定位的 Dungeons 原游戏 pak、解包网格或授权原始网格 URL。** 这不是整台机器不存在此类文件的结论，也不证明当前重建几何正确。

## 本地 Steam 范围

只读取已知 Steam 安装目录 `D:\Steam\steam` 内的以下记录：

- `steamapps\libraryfolders.vdf`
- `config\libraryfolders.vdf`
- 已登记库的 `steamapps\appmanifest*.acf`，仅读取 appid、名称与安装目录字段
- 已登记库 `steamapps\common` 的一级目录名，仅筛选含 Minecraft 或 Dungeons 的明确候选

两份库清单均只登记 `D:\steam\steam` 一处库。该库只有一个非 Dungeons 的应用安装清单；`common` 的一级目录没有 Minecraft/Dungeons 命名的安装目录。因此没有从这些安装记录定位到可进一步读取的 Dungeons pak 或解包模型。

没有广扫个人目录、其他盘、下载目录或未登记游戏文件夹，也没有下载游戏包、破解资源或改动任何游戏资产。其他位置可能存在的文件不在本次结论范围内。

## 仓库来源记录范围

只检查仓库 `_tools` 下一层 `*_ref` 目录直属的 `SOURCES.md` 和 `source_manifest.json`，共16份：

| 参考目录 | 已读来源文件 |
|---|---|
| `abaddon_ref` | `SOURCES.md` |
| `arch_visage_ref` | `SOURCES.md`、`source_manifest.json` |
| `beelzebub_ref` | `SOURCES.md` |
| `heart_of_ender_ref` | `SOURCES.md`、`source_manifest.json` |
| `leviathan_ref` | `SOURCES.md` |
| `lucifer_ref` | `SOURCES.md`、`source_manifest.json` |
| `pope_fx_ref` | `SOURCES.md` |
| `pope_ref` | `SOURCES.md`、`source_manifest.json` |
| `sunken_skeleton_ref` | `SOURCES.md` |
| `tower_guard_ref` | `SOURCES.md` |
| `tower_wraith_ref` | `SOURCES.md` |
| `vanguard_ref` | `SOURCES.md` |

其中已记录 URL 的域名只有 `minecraft.wiki`。未找到指向原始 `.fbx`、`.obj`、`.gltf`、`.glb`、`.psk`、`.pskx`、`.uasset`、`.pak` 网格/包文件的来源链接，也未找到明确授权原始网格下载的记录。现有 Wiki 图片、贴图、GIF 和音效链接不能代替原始模型网格。

[Sunken 来源记录](../../sunken_skeleton_ref/SOURCES.md) 将 `sunken_skeleton.geo.json` 明确列为 `sunken_skeleton_geo.py` 按贴图网格重建的初始几何；[Leviathan 来源记录](../../leviathan_ref/SOURCES.md) 同样将几何列为本项目重建/派生产物。它们不是已取得的 Mojang 原始网格。继承 Sunken 的比例、骨骼或对称 UV 只证明与用户指定的项目模板一致，不能独立证明 Mossy Skeleton 全身外观，更不能证明 Root Rot Armor 的未知背面和 UV 归属。

## 对当前任务的影响

用户允许的“有原始依据的左右对称共用纹理”规则保持不变。此检查没有补到新的原始几何证据，因此不能扩大对称例外、接受未知面，或解除当前暂停整合的状态。没有修改模型、贴图、UV、骨骼、来源版权说明或两份 UV 审计文件。
