# Lucifer 原始游戏资产来源

本目录只收录用户授权从本机 Minecraft Dungeons 安装目录提取的 Mossy Skeleton 与 Root Rot Armor 所需原始资产及其来源证据。安装标识为 Microsoft.Lovika，MicrosoftGame.config 的版本为 **1.17.0.0**。这里只保存相关单个包，不包含完整 PAK、游戏程序、解密密钥或无关候选装备。

## 原始身份与取用范围

- Mossy Skeleton 使用原 `SK_Skeleton` 骨骼网格，材质由 `BP_MossySkeletonCharacter` 覆盖为 `M_MossySkeleton`，其颜色贴图为 `T_MossySkeleton`，辅助贴图为 `T_Skeleton_S`。
- Root Rot Armor 对应 `NatureArmor`：`BP_NatureArmor` 实际引用 `SM_Helmet_NatureArmor`，其余躯干、左右臂、左右腿引用普通 `SproutArmor` 的五个网格；六部件统一覆盖为 `MI_NatureArmor`。这些 Sprout 网格是原始引用，不能因目录名不同而删除。
- 不包含 GrimSpooky、SproutArmor_Unique1、NatureArmor_Unique1、普通 Sprout 的头盔或颜色贴图等查错候选。
- `raw/` 保存所列相关包的原始 `.uasset/.uexp` 等条目；玩家 Skeleton/mesh、基础 Mob Blueprint 仅作为原装配与继承证据，不是 Lucifer 本体替代模型。
- `exported/` 保存 7 个原始 mesh 的 glTF/bin、4 张原始解码 PNG 和 4 组材质 props/mat。glTF 的原顶点、三角形、UV、骨骼/权重均保持导出文件字节不变，未重建成 cube、取整 UV、重绘贴图或添加颜色补偿。
- `evidence/` 保存原 Blueprint 属性赋值和逐面几何/纹理核验。未序列化的变换不被声明为实测 identity；原玩家 socket 与 Mossy Skeleton 怪物挂点也没有被等同。

## 校验链与工具

原包由项目的精确 PAK 条目读取脚本 `pak_index.py` 提取：读取本地 legacy PAK v8 索引，仅解压选定条目，并将所得 payload SHA-1 与 PAK 条目 SHA-1 比较。复制到本目录前再次验证每个原文件的大小、SHA-1 和 SHA-256，复制后再验证 SHA-256。

`source_manifest.json` 逐文件记录：正式相对路径、原始 PAK 文件、条目路径、条目 SHA-1、原/副本 SHA-256、导出来源包。上游校验清单为本机 `work/lucifer_original/raw_manifest.json`，本目录仅列已筛选条目。

网格/PNG/材质附件由 [UE Viewer / UModel 官方仓库](https://github.com/gildor2/UEViewer) 的可执行文件导出；本次记录的导出器为 **UE Viewer build 1590**，使用 `-game=ue4.22`、`-export -gltf -png`。下载来源为官方仓库的 [umodel.exe](https://raw.githubusercontent.com/gildor2/UEViewer/master/umodel.exe)，实际可执行文件 SHA-256 见清单。PAK 结构读取参考 [CUE4Parse 官方源代码](https://github.com/FabianFG/CUE4Parse/tree/master/CUE4Parse/UE4/Pak)。这些工具不随本目录分发。

glTF 使用 UModel 的坐标转换：原 Unreal Z-up/厘米转换为 glTF Y-up/米。它是导出表示形式，不是原 `.uasset` 的二进制格式；原包始终另存以便追溯。mesh 内默认材质名称仍可能写 `MI_Skeleton` 或 `MI_SproutArmor`，正确运行时覆盖必须以 Blueprint 证据为准。

## 纹理和材质的实际验证范围

`T_NatureArmor` 与 Wiki Root Rot 贴图的 alpha 全部一致，3377 个可见像素的 RGBA 差异为 0；719 个全透明像素的隐藏 RGB 不同，本目录保留游戏导出的隐藏颜色。`T_NatureArmor_S` 与既有 Wiki ShadowTexture 的 4096 个 RGBA 像素全部一致。Mossy 贴图采用实际游戏解码文件。

UModel glTF 中的 baseColorFactor/metallic/roughness 是导出器调试材质，不能用它评判原作配色。[官方 glTF 导出源码](https://github.com/gildor2/UEViewer/blob/master/Exporters/ExportGLTF.cpp)也未将原 Unreal 母材质完整移植进去。`.mat` 中的纹理用途来自名称启发式；`.props.txt` 保留所支持的原参数，但并非完整 shader。

本目录保留 `M_MasterEquipment` 与 `Master_ModelMaterial` 原包和参数导出；没有追取它们全部 noise/VFX 二级依赖，也没有重建 Unreal 光照、曝光、Bloom 或完整母材质公式。Blockbench 的纹理预览因此不能被声称为原游戏逐像素渲染复现。Nature 的参数确有 NaturalEmissive=0.7、Emissive=(0.69331,8,0,1)、ConstantEmissive=true，但不能据参数名称替各通道发明公式或颜色补偿。

## 本地保存范围

本目录是当前项目的本地原始参照与导入输入。没有上传、发布、推送、打包整套游戏资源，也没有修改本机游戏安装文件。资产版权仍属于原权利方；本文件不授予额外再分发许可。

## 后续原始静态发光移植

本目录初次整理后，已进一步解析 MI_NatureArmor 的原始 shader resource、UniformExpressions 和匹配的 SM5 DXBC，确认静态默认发光公式并接入 Blockbench。完整证据见 [material_port/MI_NatureArmor_uniform_mapping.md](material_port/MI_NatureArmor_uniform_mapping.md)，新增文件独立清单见 [material_port/manifest.json](material_port/manifest.json)。此更新确认的是原材质静态发光运算，仍不声称移植了完整游戏场景灯光、曝光、Bloom 和动态运行时覆盖。

注意原 compiled 分支中 `SpecularTexture=False`；早期 `.props.txt` 中某个静态开关的 value 若 `bOverride=false`，不能单独当作实际编译值。保留原 `.props` 文件不改，以 compiled 描述和表达式证据解释有效开关。
