# 精英词缀原图检索 A：迅捷、铁壁、狂怒、吸血

日期：2026-11-23。依据同目录上级 `ART-BRIEF.md` 追加规格：原生16×16、Alpha仅0/255、2–3种颜色、粗轮廓，在约8像素高时仍可辨认；主色及指定形状都必须符合。**本组4项均建议新绘，没有认定可直接使用的原图。**

## 检索和实测方法

- 本地原包索引：`D:/agent/dungeons_extract/index/pak_files.json`；原包目录：`D:/XboxGames/Minecraft Dungeons/Content/Dungeons/Content/Paks`。
- 定点检索 Swiftfooted、SpeedSynergy、SpiritSpeed、Swiftness、Protection、Shielding、DefenseUp、ShieldVFX、WildRage、Frenzied、Strength、Leeching、EvokerFangs 等词；检查附魔、状态图标及相关纹理，不以名称相近代替实际造型判断。
- 使用既有 CUE4Parse 导出器及 UE4.22 版本参数，定点导出17个Texture2D，17个成功、0个失败；保留导出原PNG的尺寸和像素，未改色、缩图或清理透明度。
- 每张均实际目视原图及仅在内存中生成的8px最近邻观察图；观察图未写盘。表中色数为Alpha>0的不同RGB数量，透明度按PNG实测，未把视觉相近的颜色算成一色。
- 原导出在 `_inspection_affixes_a/assets/`；Frenzied追加2张在 `_inspection_affixes_a/frenzied/assets/`。上述目录下保留同包结构的PNG，以及对应metadata和导出记录。未修改旧18张、`REPORT.md`或项目代码。

## affix_swift 迅捷（#62D9E8）

结论：新绘。

| 原包完整路径 | 原尺寸 | 可见RGB色数 | Alpha实测 | 实际造型及未采用理由 |
|---|---:|---:|---|---|
| `Dungeons/Content/UI/Materials/StatusEffect/GameplayEffect/swiftness_icon.uasset` | 103×94 | 3 | 0、255 | 青色块状疾行/足部符形，只有3色和二值透明，是配色最接近的候选；但原尺寸103×94，且更像块状靴部而非明确向右风痕或翅膀，不能原尺寸直用。 |
| `Dungeons/Content/UI/Materials/StatusEffect/GameplayEffect/T_Buff_Swiftness_Icon.uasset` | 40×40 | 5 | 255 | 青白足部及速度线，深蓝方形背景；40×40、5色、完全不透明，非16px透明单风痕。 |
| `Dungeons/Content/Components/Enchantments/Swiftfooted/T_Swiftfooted_Icon.uasset` | 256×256 | 5 | 15档 | 蓝色菱形卡面中为足部/旋动形，非单独右向风痕；256×256、5色并有半透明边缘。 |
| `Dungeons/Content/Components/Enchantments/SpeedSynergy/T_SpeedSynergy_Icon.uasset` | 256×256 | 6 | 15档 | 蓝色菱形底牌内为药瓶/速度符号，不是单独向右风痕或翅膀；256×256、6色并有半透明边缘。 |
| `Dungeons/Content/Components/Enchantments/SpiritSpeed/T_SpiritSpeed_Icon.uasset` | 256×256 | 5 | 15档 | 蓝色菱形底牌中含多个白色灵魂及足部形，形状复杂；不是单个向右青色风痕或翅膀。 |

## affix_iron 铁壁（#B5B5B5）

结论：新绘。

| 原包完整路径 | 原尺寸 | 可见RGB色数 | Alpha实测 | 实际造型及未采用理由 |
|---|---:|---:|---|---|
| `Dungeons/Content/Effects/Materials/Items/T_ShieldVFX.uasset` | 16×16 | 8 | 0、254、255 | 唯一原生16×16候选，但为纯红绿为主的盾形通道遮罩，含8色和Alpha254，不是可直接显示的钢灰方盾。不能将材质通道贴图硬当成品图标。 |
| `Dungeons/Content/Components/Enchantments/Protection/T_Protection_Icon.uasset` | 256×256 | 10 | 12档 | 银色盾主体放在蓝色菱形附魔底牌中，轮廓偏长尖盾而非方盾；256×256、10色和半透明边缘均不符。 |
| `Dungeons/Content/Components/Enchantments/Shielding/T_Shielding_Icon.uasset` | 256×256 | 39 | 233档 | 橙红菱形底牌与成组银色盾/柱形构图，非钢灰单面方盾；256×256、39色及大量半透明。 |
| `Dungeons/Content/UI/Materials/StatusEffect/GameplayEffect/T_Buff_DefenseUp_Icon.uasset` | 40×40 | 11 | 255 | 银灰长盾置于绿色方形背景内；40×40、11色、完全不透明，非透明钢灰方盾。 |
| `Dungeons/Content/UI/Materials/Boss/T_ImmuneShield.uasset` | 152×202 | 3722 | 158档 | 紫粉渐变尖底盾及中心斜交符号，非钢灰方盾；152×202、3722色、大量半透明。 |

## affix_rage 狂怒（#FF6B5E）

结论：新绘。

| 原包完整路径 | 原尺寸 | 可见RGB色数 | Alpha实测 | 实际造型及未采用理由 |
|---|---:|---:|---|---|
| `Dungeons/Content/Components/Enchantments/WildRage/T_WildRage_Icon.uasset` | 256×256 | 7 | 12档 | 红色菱形底牌中为怒脸，怒眉语义接近，但含耳/嘴等整张面孔而非简洁怒眉；256×256、7色、半透明。8px时面部只剩方环/嘴形。 |
| `Dungeons/Content/Components/Enchantments/Frenzied/T_Frenzied_Icon.uasset` | 256×256 | 8 | 0、1、3、5、6、9、255 | 红色人物怒脸连同亮黄头部细节、左侧长剑置于菱形卡面；怒脸语义相近但构图复杂，256×256、8色并有半透明。 |
| `Dungeons/Content/UI/Materials/StatusEffect/GameplayEffect/T_Buff_Frenzied_Icon.uasset` | 40×40 | 10 | 255 | 红色怒脸连同左侧长剑及黄色头部细节，深红方形背景；40×40、10色、完全不透明，不符合2–3色的拳头/怒眉小标。 |
| `Dungeons/Content/UI/Materials/StatusEffect/GameplayEffect/strength_icon.uasset` | 103×103 | 3 | 0、255 | 橙红色斜剑，虽然仅3色、二值透明，形状不是握拳或怒眉，尺寸103×103，主色也偏橙。 |
| `Dungeons/Content/UI/Materials/StatusEffect/GameplayEffect/T_Buff_StrengthUp_Icon.uasset` | 40×40 | 18 | 255 | 橙红爆发背景中的斜剑；40×40、18色、完全不透明，非握拳或怒眉。 |

## affix_leech 吸血（#D97AD9）

结论：新绘。

| 原包完整路径 | 原尺寸 | 可见RGB色数 | Alpha实测 | 实际造型及未采用理由 |
|---|---:|---:|---|---|
| `Dungeons/Content/Components/Enchantments/Leeching/T_Leeching_Icon.uasset` | 256×256 | 6 | 15档 | 红色菱形附魔卡面，中心是成组尖牙/吸血符形，既非粉紫主色，也非一颗独立滴血獠牙；8px观察时内部细节并成红团。 |
| `Dungeons/Content/Actors/Characters/Enemies/Illagers/Evoker/Fang/T_EvokerFangs.uasset` | 64×64 | 11 | 0、255 | 唤魔者尖牙的棕灰模型展开贴图，多个分离表面，没有独立的粉紫单颗獠牙及血滴；64×64、11色。 |

## 供新绘使用的简化重点

- 迅捷：采用一个右向尖端和2–3条粗短风痕，主块为青色；避免脚、鞋、药瓶等替代含义。
- 铁壁：方盾保持平顶和宽底，用一条钢灰亮边加暗色面，不附带菱形卡面或光效。
- 狂怒：握拳或一组明确下压怒眉二选一，避免同时塞进整张人脸、火焰和武器。
- 吸血：一颗宽根弯尖獠牙，单独保留一滴粉紫血；避免多个牙齿形成嘴巴或爪痕。

本报告只说明已检索、导出并实际查看的候选不满足本次规格，不声称整个游戏中不存在其他可以改造的纹理。对原图改色、裁切、重采样会构成改绘，不应记录为“原尺寸原图直接采用”。

