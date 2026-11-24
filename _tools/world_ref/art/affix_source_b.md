# 精英词缀原图检索 B

2026-11-23，负责 `affix_frost`、`affix_venom`、`affix_burst`、`affix_summon`。查阅完整游戏包索引 `D:/agent/dungeons_extract/index/pak_files.json`，检索 frost、snow、ice、chill、poison、venom、bomb、explod、skull、summon、soul 等命名，按精确包路径导出以下8张候选，全部实际目视。

使用既有 `D:/agent/dungeons_extract/exporter/bin/Release/net8.0/exporter.exe`，UE4.22，8对象成功、0失败；游戏包只读。原尺寸 PNG 及元数据位于 `art/_inspection_affix_b/`，未缩放、裁切或重染候选图，未修改旧资产和 REPORT.md。

下表原包路径相对于 `Dungeons/Content/`，扩展名为 `.uasset`；PNG 路径统一为 `_inspection_affix_b/assets/Dungeons/Content/` 加表内路径，并将扩展名换为 `.png`。色数仅统计可见 RGB。

| 原包路径 | 原尺寸 | 色数 | Alpha | 实际画面与决定 |
| --- | --- | ---: | --- | --- |
| `Effects/Materials/Ice/T_IceSymbol` | 6×6 | 1（白） | 0、255 | 粗短雪花，语义匹配寒霜；保留原尺寸作为来源参考，它本身不是最终16文件。 |
| `Components/Enchantments/Chilling/T_Chilling_Icon` | 256×256 | 8 | 15档 | 蓝色雪花附魔图，带大面积UI底和横条，未达到16、2–3色与二值透明。拒作最终图。 |
| `Components/Enchantments/Snowing/T_Snowing_Icon` | 256×256 | 7 | 15档 | 带拖尾雪球与UI底，不是单片雪花。拒用。 |
| `Components/Enchantments/PoisonedMelee/T_PoisonedMelee_Icon` | 256×256 | 8 | 15档 | 绿毒云附魔图，带底，不是单一毒滴。拒用。 |
| `UI/Materials/StatusEffect/GameplayEffect/T_Buff_Poisoned_Icon` | 40×40 | 6 | 全255 | 绿色骷髅与不透明深底；既非毒滴也无透明外轮廓。拒用。 |
| `Components/Enchantments/Exploding/T_Exploding_Icon` | 256×256 | 9 | 10档 | 粉黄爆炸光与UI底，无炸弹和引线。拒用。 |
| `Effects/Materials/Skull/T_SkullSoul` | 7×7 | 1（白） | 0、255 | 单枚小骷髅，轮廓可辨。可作为原版造型参考；三枚原宽横排至少21像素，无法不缩放放进16网格。 |
| `Effects/Materials/Skull/T_ShadowSkull` | 7×7 | 1（白） | 0、255 | 同为单枚小骷髅，不是三枚横排；同上。 |

## 建议采用方式

- **寒霜**：原版 `T_IceSymbol` 是语义贴合的参考部件，但仅6×6、单白色，不满足本次最终字形的16×16、2–3色、指定主色 `#E8F4FF` 和粗同色轮廓要求，因此仍然新绘。原图保留给后续按简报裁补，本次不补边、不改色、不缩放。
- **剧毒**：新绘16×16毒液滴，以 `#70DB70` 为主色，2–3色、二值透明，缩小后优先读成滴形。
- **爆裂**：新绘16×16带引线火星的炸弹，以 `#FFA15C` 为主色；原版爆炸特效不能替代炸弹剪影。
- **召唤**：新绘三枚约4像素宽的骷髅横排，以 `#A276BE` 为主色；可参考原版7×7骷髅的眼窝和齿部语言，但不缩小或拼接原图冒充原尺寸素材。

这些候选没有声称均为可直接使用的16×16成品。尤其附魔图大分辨率UI底、原版单骷髅宽度与三枚横排的约束均已明确记录。

## 原尺寸参考部件交付与校验

以下三份已复制到 `art/dungeons/`；复制后与本次从原包导出的源 PNG 逐字节一致。它们仅作为原版参考部件；本批11张最终词缀均采用符合指定主色、2–3色与16×16要求的新绘字形。

| 参考 PNG | 精确原包路径 | 原尺寸 | SHA-256 |
| --- | --- | --- | --- |
| `dungeons/T_IceSymbol.png` | `Dungeons/Content/Effects/Materials/Ice/T_IceSymbol.uasset` | 6×6 | `e566e476df5dfec089c8bf77b8934fcd118896c8e3726bb757ceefa046d9466e` |
| `dungeons/T_SkullSoul.png` | `Dungeons/Content/Effects/Materials/Skull/T_SkullSoul.uasset` | 7×7 | `8045daf014b74ebea6994c7ec3b6fc6d8942d48fbc002b2dec55d113451ceb20` |
| `dungeons/T_ShadowSkull.png` | `Dungeons/Content/Effects/Materials/Skull/T_ShadowSkull.uasset` | 7×7 | `b3518848789d79a2574f81c938298c6b54fa3bc577cdf3f2561a4e3c5d76854d` |
