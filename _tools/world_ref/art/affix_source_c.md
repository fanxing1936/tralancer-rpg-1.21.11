# 词缀原图检索 C：罪染、圣印、首领

2026-11-23。先检索本机完整索引 `D:/agent/dungeons_extract/index/pak_files.tsv`，再实际查看既有导出和四份定点原尺寸导出。三项均建议新绘，以满足指定主色、16×16、2–3色及字号可读性。

定点导出工具：`D:/agent/dungeons_extract/exporter/bin/Release/net8.0/exporter.exe`，CUE4Parse，解析版本 UE4.22。游戏包只读，输出 `_inspection_affix_c/`；四对象成功、零失败，未缩放或改色。导出记录在该目录 `export_report.json`。

| 词缀 | 实际查看的原包路径 | 原尺寸 / 可见 RGB 色数 / Alpha档数 | 采用建议 |
| --- | --- | --- | --- |
| `affix_taint` 罪染 | `Dungeons/Content/Content_DLC6/Actors/Characters/Enemies/Endersent/T_EyeofEnder.uasset` | 13×13 / 12 / 2（0、255） | 眼睛轮廓清楚，但主色是绿色，没有裂痕。不能当暗紫红 `#C86A92` 裂眼直接使用。新绘。 |
| `affix_taint` 罪染 | `Dungeons/Content/Content_DLC5/Actors/Items/GuardianEye/T_GuardianEye_GearIcon.uasset` | 24×24 / 24 / 3 | 浅青灰机械方框包围绿色眼心，既非裂眼、也非指定紫红主色。新绘。 |
| `affix_taint` 罪染 | `Dungeons/Content/UI/Materials/Currency/T_EyeOfEnder_Currency.uasset` | 72×72 / 288 / 2 | 绿眼货币图，有额外底板与较多过渡颜色，不符合紫红裂眼。新绘。 |
| `affix_holy` 圣印 | `Dungeons/Content/Components/Enchantments/RadianceMelee/T_RadianceMelee_Icon.uasset` | 256×256 / 6 / 15 | 明确有白热中心与四向金色十字，可作为构图参考；外围含大片红橙光、分枝和多档半透明，不是指定金色2–3色的透明小十字，不能直接采用。新绘。 |
| `affix_holy` 圣印 | `Dungeons/Content/Components/Enchantments/RadianceRanged/T_RadianceRanged_Icon.uasset` | 256×256 / 6 / 15 | 除十字外带贯穿画面的横条和红底块，构图更像附魔UI纹理，字号下会拥挤。新绘。 |
| `affix_holy` 圣印 | `Dungeons/Content/Effects/Materials/Stars/T_Stars_16.uasset` | 32×32 / 1 / 4（0、63、127、255） | 四颗白星图集，右上格可参考短粗四向射线；无金色且含半透明，不能直接充当独立金十字。新绘。 |
| `affix_champion` 首领 | `Dungeons/Content/Actors/Equipment/Armor/ChampionsArmor_Unique1/T_ChampionsArmor_Unique1_Icon.uasset` | 512×512 / 3455 / 240 | 目视为银灰金色盔甲装备图，名称的 Champion 并不表示皇冠；不是小王冠，字号下复杂。新绘。 |

完整索引没有 `T_*Crown*` 纹理名称命中。场景或角色模型上的冠饰与本次独立小王冠图标不同；不把角色材质或渲染截图冒充原包物品图。

## 实际查看的 PNG 位置

既有导出：

- `D:/agent/dungeons_extract/colorscan/tex/assets/Dungeons/Content/Content_DLC6/Actors/Characters/Enemies/Endersent/T_EyeofEnder.png`
- `D:/agent/dungeons_extract/upgrade/icons_jq/assets/Dungeons/Content/Actors/Equipment/Armor/ChampionsArmor_Unique1/T_ChampionsArmor_Unique1_Icon.png`
- `D:/agent/dungeons_extract/upgrade/michael_fx/assets/Dungeons/Content/Effects/Materials/Stars/T_Stars_16.png`

本轮定点导出，路径均相对本目录：

- `_inspection_affix_c/assets/Dungeons/Content/Components/Enchantments/RadianceMelee/T_RadianceMelee_Icon.png`
- `_inspection_affix_c/assets/Dungeons/Content/Components/Enchantments/RadianceRanged/T_RadianceRanged_Icon.png`
- `_inspection_affix_c/assets/Dungeons/Content/Content_DLC5/Actors/Items/GuardianEye/T_GuardianEye_GearIcon.png`
- `_inspection_affix_c/assets/Dungeons/Content/UI/Materials/Currency/T_EyeOfEnder_Currency.png`

## 三骷髅横排的粗轮廓建议

16×16可使用三个4×6的小头，横坐标分别为1–4、6–9、11–14，中间各留1格透明间隙。头盖骨约4×4，下颌收成2格；每头两眼各1格，省略鼻孔与细牙。三个头宜处在同一水平，避免对角堆叠。

8px字号下每头只剩约2×3格，因此保留亮色头盖、单格暗眼带和单格窄颌即可。务必在缩小采样后核对三个分离亮头是否仍然可数；不要为了逐个保留双眼而让它们变成一串碎点。此段只作构图建议，没有绘制图片。
