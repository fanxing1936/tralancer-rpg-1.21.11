# Verdant Robe 原始资产来源包

本目录仅保留用户本机 Minecraft Dungeons **1.17.0.0** 中本次 Verdant Robe 所需资产与核验证据。原始资源版权归 Mojang Studios / Microsoft 及其权利人所有；本项目文件不产生新的资源授权，不将这些提取资产当作自制可自由分发素材。本目录供用户本地复刻、编辑和核验使用；未上传网络、未包含整包 PAK、密钥或提取工具二进制。

## 身份与内容

用户指定 [Verdant Robe](https://minecraft.wiki/w/Dungeons:Verdant_Robe)。Wiki 页面直接请求受限，搜索缓存给出内部名 SageRobe，[Ancient Hunt 表](https://minecraft.wiki/w/Dungeons:Ancient_Hunt)对应 EvocationRobe_Unique2。本机原物品 Instance CDO 的 ItemIdName / SerializedId、GearActor 及其 BP 组件赋值构成实际身份链；原游戏图标可见绿帽、银扣、绿袍银边。未声称已与 Wiki 图片逐像素相同。

包内包含 12 个原 UE package（24 个 uasset/uexp）、四件原网格的 glTF/bin、两张原材质 PNG、两张原图标 PNG、原 MI props/mat，以及 BP/材质/装配/导入和独立回读证据。四件网格共 **128 顶点、64 三角形**：SageHat、MageRobe_Evocation、L_Arm_EvocationRobe、R_Arm_EvocationRobe。没有候选重建、UV 重画或 cube 化。

`T_EvocationRobe_Unique1_S` 是本套 `MI_EvocationRobe_Unique2` 的实际 Specular 引用，属于必要依赖；其 Unique1 目录名不表示误混其他盔甲。母材质 `M_MasterEquipment` 原包保留用于材质证据；它的所有 noise/VFX 二级依赖没有扩展抓取。

原玩家骨架是装配依赖。`evidence/verdant_player_bind_source.json` 保存直接解码的原 binary inverseBindMatrices、节点和源哈希，不重复复制玩家整个角色网格。原 `J_Head_Socket` 及直接骨挂点/组件字节证据见 assembly、identity 文件。历史临时绝对路径保留作为审计记录，当前包内对应文件以 `source_manifest.json` 相对路径为准。

## 来源与校验

所有原 package payload 均在提取时与 PAK 条目 SHA-1 实读比较后写出；本次复制前再次重算 SHA-1 / SHA-256，复制后再核对 SHA-256。`source_manifest.json` 对每个文件给出路径、字节数、SHA-256，原包另含原 PAK 文件名、条目路径与已验证 SHA-1。清单本身不自我哈希。

原 glTF/bin/PNG 使用 [UE Viewer 官方工具](https://github.com/gildor2/UEViewer) build 1590、`-game=ue4.22 -export -gltf -png` 从临时原包导出，原工具 SHA-256 为 `13502e5a4d8f6b5f32252afebd6360f7302ccfaccf6b8dda65beff0be2d364a0`。工具来源为官方仓库的 [umodel.exe](https://raw.githubusercontent.com/gildor2/UEViewer/master/umodel.exe)。未改动游戏安装或源包。

## 实际原生保存验证

`../separate/verdant_robe_original.bbmodel` 已由主任务通过 Blockbench 原生导入、保存。独立文件回读直接比较原 glTF/bin、原骨架二进制 bind 与实际 bbmodel；不是用导入 JSON 自证。报告保存在 `../separate/verdant_original_validation.json` / `.md`，包内 evidence 留同版副本。

四件原网格的坐标、UV0、三角顺序、刚性绑定和父级差异均为 0；两张内嵌 PNG 与原字节相等。原组件非均匀缩放逐点烘入，反算原局部坐标残差和骨四元数/Euler 表示残差在报告中如实给出。全部 64 个源三角形到 native 面的对应保留。原 normals/tangents/UV1 由 sidecar 保存和核验，未声称已被原生 importer 消费。

原 UV 有 1288 个不透明有效图案像素，其中 85 个未被这四件原网格正面积覆盖，29 个被多个原面共用。这是原件数据，不能为填满纹理或消除复用而改 UV。

## 装配和材质边界

装配依据原玩家 binary bind、实际 BP socket/骨挂点和组件 TRS。省略 native 字段采用明确标注的标准默认值；native Paperdoll 骨架赋值与参考图运行时姿势仍非本报告已证实事项。刚性权重是依据原挂点派生，原 StaticMesh 自身没有蒙皮权重。

原材质 Emissive 是白色 (1,1,1)，NaturalEmissive 为 0.699999988079071。native compiled 描述证明本套 SpecularTexture=True、ConstantEmissive=True；不是把所有 props 数值当作有效开关。保存工程包含原两张 PNG 和原始静态发光移植 metadata。独立几何核验不凭 metadata 宣称完整 Unreal 母材质、高光/粗糙度、Bloom、曝光与场景光照等价；实际 shader 执行及游戏/动画检查由主任务单独记录。

`material_port/` 封存主任务已固定的三份 uniform/匹配/反汇编清单，以及实际 PS `17d7f0ed06ee1cba9b4141f6a8466432829f043d` 的 DXBC 和 asm。主任务由这些原程序确认静态发光为在线性色彩空间中 `S.B * [1,1,1] + Albedo * 0.699999988079071`（原静态 EmissivePower / DeathEmissive 均为 1）；不是上一套盔甲的绿色高强度参数。材质纹理按原默认 sRGB 解码，未把发光烘进 Albedo。只封存明确相关 shader，不包含整份游戏 shader 库。
