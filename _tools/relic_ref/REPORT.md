# 圣物图标交付

按《RELIC-ART-PROMPT》交付 74 张原生 16×16 RGBA PNG。74 张均为本批逐像素新绘，直接采用的地下城原图为 0 张。可见颜色数为 3–10，透明度逐像素核对为 0 或 255。

[图标总览](art/PREVIEW.png)在深、浅底上各排一组原尺寸与 4 倍最近邻放大图。表内色数按各交付文件的完全不透明像素统计。

## 原包筛选

在本机地下城包索引中按物品及图形筛选，再查看候选 PNG 的原尺寸、轮廓与颜色。下列路径从 Dungeons/Content/ 起算。

| 候选原包路径 | 尺寸 | 筛选结果 |
| --- | ---: | --- |
| `Decor/Prefabs/_Fruit_Food/T_Bottle.uasset` | 16×16 | 绿色瓶身表面展开图。空瓶、圣水与药水分别绘制独立瓶形。 |
| `Actors/Items/Potions/HealthPotion/T_HealthPotion_Icon_inventory.uasset` | 256×256 | 对药水相关的 24 张候选逐张量过尺寸。瓶纹样及材质多为 32 或 64 像素，各档瓶形与液体标志在本次 16 格画布中绘制。 |
| `Effects/Materials/Feather/T_Feathers.uasset`、`Effects/Flairs/RespawnFlairs/03/T_Feathers.uasset` | 各 16×16 | 完整淡色羽毛。谦卑之羽另画断轴，断羽另画焦边与分离的羽根。 |
| `Actors/Items/Food/Food2/T_Apple_Minecraft.uasset` | 16×16 | 完整亮红苹果。禁果需要暗红色与咬痕，腐宴残食另有腐斑与苍蝇。 |
| `Patch2/Actors/Items/SoulLantern/T_SoulLantern_GearIcon.uasset` | 24×24 | 与青焰笼灯题材接近，封魔灯按 16 格重新安排火芯和铁笼。 |
| `Effects/Flairs/RespawnFlairs/03/T_Bell.uasset`、`Decor/Prefabs/Book/T_Book.uasset` | 64×64、32×32 | 分别为表面贴图。手摇铃采用木柄和铜质外壳，六本传承书共用一套书脊、包角和书页。 |
| `Decor/Prefabs/_Lab/Paper/T_Paper_Graph_02.uasset` | 32×32 | 旧图纸素材。本批碎片沿用项目卷轴的暖纸和褐色线稿，重新绘制缺角。 |
| `Components/Enchantments/Chains/T_Chain.uasset` | 10×6 | 灰白横向链环。封印链按七件物体的宽度另绘金色回环和暗孔。 |
| `Content_DLC3/Decor/Prefabs/_Mountains/Gale_Sanctum_Props/GS_Lantern_Hanging_01/T_Gold_Chain.uasset` | 16×16 | 场景金链以纵向排列，供绘制时比对金属明暗。 |

## 七柱武器核心

剪影依次为蛇矛、锚、镰刀、太刀、弩、匕首和弓。对应关系来自项目的 pact_weapon1 到 pact_weapon7 发放定义与资源包物品模型。残页、封印链和罪核各用同一套外形，柱色与内部图案随领主变化。

## 逐项清单

### 驱魔器具

| PNG | 物品 | 来源 | 可见色数 |
| --- | --- | --- | ---: |
| [rite_doll.png](art/rite_doll.png) | 替死人偶 | 原生新绘 | 8 |
| [rite_star.png](art/rite_star.png) | 天启星 | 原生新绘 | 9 |
| [holy_water.png](art/holy_water.png) | 驱魔圣水 | 原生新绘 | 9 |
| [strong_water.png](art/strong_water.png) | 浓缩驱魔圣水 | 原生新绘 | 10 |
| [rite_nail.png](art/rite_nail.png) | 银质圣钉 | 原生新绘 | 5 |
| [rite_bell.png](art/rite_bell.png) | 告解铃 | 原生新绘 | 8 |
| [rite_incense.png](art/rite_incense.png) | 净罪香 | 原生新绘 | 8 |
| [rite_lantern.png](art/rite_lantern.png) | 封魔灯 | 原生新绘 | 9 |
| [chalk_1.png](art/chalk_1.png) | 守御粉笔 | 原生新绘 | 8 |
| [chalk_2.png](art/chalk_2.png) | 压制粉笔 | 原生新绘 | 8 |
| [chalk_3.png](art/chalk_3.png) | 疾行粉笔 | 原生新绘 | 8 |
| [medium_1.png](art/medium_1.png) | 谦卑之羽 | 原生新绘 | 5 |
| [medium_2.png](art/medium_2.png) | 无主之潮 | 原生新绘 | 7 |
| [medium_3.png](art/medium_3.png) | 不眠之钟 | 原生新绘 | 6 |
| [medium_4.png](art/medium_4.png) | 腐宴残食 | 原生新绘 | 8 |
| [medium_5.png](art/medium_5.png) | 熄怒之雪 | 原生新绘 | 6 |
| [medium_6.png](art/medium_6.png) | 清醒之镜 | 原生新绘 | 7 |
| [medium_7.png](art/medium_7.png) | 自愿之金 | 原生新绘 | 5 |

### 真名残页

| PNG | 物品 | 来源 | 可见色数 |
| --- | --- | --- | ---: |
| [page_1.png](art/page_1.png) | 路西法残页 | 原生新绘 | 6 |
| [page_2.png](art/page_2.png) | 利维坦残页 | 原生新绘 | 6 |
| [page_3.png](art/page_3.png) | 亚巴顿残页 | 原生新绘 | 6 |
| [page_4.png](art/page_4.png) | 别西卜残页 | 原生新绘 | 6 |
| [page_5.png](art/page_5.png) | 萨麦尔残页 | 原生新绘 | 6 |
| [page_6.png](art/page_6.png) | 贝利尔残页 | 原生新绘 | 6 |
| [page_7.png](art/page_7.png) | 玛门残页 | 原生新绘 | 6 |

### 裁决罪物

| PNG | 物品 | 来源 | 可见色数 |
| --- | --- | --- | ---: |
| [sealed_1.png](art/sealed_1.png) | 路西法封印罪物 | 原生新绘 | 9 |
| [sealed_2.png](art/sealed_2.png) | 利维坦封印罪物 | 原生新绘 | 8 |
| [sealed_3.png](art/sealed_3.png) | 亚巴顿封印罪物 | 原生新绘 | 8 |
| [sealed_4.png](art/sealed_4.png) | 别西卜封印罪物 | 原生新绘 | 8 |
| [sealed_5.png](art/sealed_5.png) | 萨麦尔封印罪物 | 原生新绘 | 8 |
| [sealed_6.png](art/sealed_6.png) | 贝利尔封印罪物 | 原生新绘 | 8 |
| [sealed_7.png](art/sealed_7.png) | 玛门封印罪物 | 原生新绘 | 8 |
| [core_1.png](art/core_1.png) | 路西法武器核心 | 原生新绘 | 7 |
| [core_2.png](art/core_2.png) | 利维坦武器核心 | 原生新绘 | 7 |
| [core_3.png](art/core_3.png) | 亚巴顿武器核心 | 原生新绘 | 7 |
| [core_4.png](art/core_4.png) | 别西卜武器核心 | 原生新绘 | 7 |
| [core_5.png](art/core_5.png) | 萨麦尔武器核心 | 原生新绘 | 7 |
| [core_6.png](art/core_6.png) | 贝利尔武器核心 | 原生新绘 | 7 |
| [core_7.png](art/core_7.png) | 玛门武器核心 | 原生新绘 | 6 |

### 传承书

| PNG | 物品 | 来源 | 可见色数 |
| --- | --- | --- | ---: |
| [legacy_pope.png](art/legacy_pope.png) | 教皇传承 | 原生新绘 | 8 |
| [legacy_usurper.png](art/legacy_usurper.png) | 篡位者传承 | 原生新绘 | 8 |
| [legacy_jacques.png](art/legacy_jacques.png) | 雅克传承 | 原生新绘 | 10 |
| [legacy_saul.png](art/legacy_saul.png) | 扫罗传承 | 原生新绘 | 10 |
| [legacy_michael.png](art/legacy_michael.png) | 米迦勒传承 | 原生新绘 | 10 |
| [legacy_lucifer.png](art/legacy_lucifer.png) | 路西法传承 | 原生新绘 | 9 |

### 新物品

| PNG | 物品 | 来源 | 可见色数 |
| --- | --- | --- | ---: |
| [empty_vial.png](art/empty_vial.png) | 空瓶 | 原生新绘 | 8 |
| [blank_rite.png](art/blank_rite.png) | 空白圣具 | 原生新绘 | 5 |
| [blueprint_fragment.png](art/blueprint_fragment.png) | 图纸碎片 | 原生新绘 | 8 |

### 药水

| PNG | 物品 | 来源 | 可见色数 |
| --- | --- | --- | ---: |
| [potion_blood.png](art/potion_blood.png) | 精血药水 | 原生新绘 | 7 |
| [potion_decay.png](art/potion_decay.png) | 衰败药水 | 原生新绘 | 7 |
| [potion_beast.png](art/potion_beast.png) | 动物朋友 | 原生新绘 | 7 |
| [potion_soothe.png](art/potion_soothe.png) | 镇痛药水 | 原生新绘 | 7 |
| [potion_fireproof.png](art/potion_fireproof.png) | 抗火药水 | 原生新绘 | 6 |
| [potion_cleanse.png](art/potion_cleanse.png) | 净口药水 | 原生新绘 | 6 |
| [potion_venom.png](art/potion_venom.png) | 剧毒药水 | 原生新绘 | 7 |
| [potion_revive.png](art/potion_revive.png) | 复生药水 | 原生新绘 | 7 |
| [potion_shield.png](art/potion_shield.png) | 护盾药水 | 原生新绘 | 6 |
| [potion_fatigue.png](art/potion_fatigue.png) | 疲惫药水 | 原生新绘 | 7 |
| [potion_vigor.png](art/potion_vigor.png) | 体能药水 | 原生新绘 | 7 |
| [potion_stone.png](art/potion_stone.png) | 石肤药水 | 原生新绘 | 6 |
| [potion_shadow.png](art/potion_shadow.png) | 影行药水 | 原生新绘 | 7 |
| [potion_blaze.png](art/potion_blaze.png) | 烈焰药水 | 原生新绘 | 7 |
| [potion_exorcise.png](art/potion_exorcise.png) | 驱邪药水 | 原生新绘 | 7 |
| [potion_prayer.png](art/potion_prayer.png) | 祷告药水 | 原生新绘 | 6 |
| [potion_rite.png](art/potion_rite.png) | 血祭药水 | 原生新绘 | 7 |
| [potion_frenzy.png](art/potion_frenzy.png) | 血战药水 | 原生新绘 | 9 |
| [potion_undying.png](art/potion_undying.png) | 不灭药水 | 原生新绘 | 9 |
| [potion_lure.png](art/potion_lure.png) | 引潮药水 | 原生新绘 | 9 |

### 试炼与失乐园

| PNG | 物品 | 来源 | 可见色数 |
| --- | --- | --- | ---: |
| [trial_key.png](art/trial_key.png) | 试炼之匙 | 原生新绘 | 3 |
| [ominous_key.png](art/ominous_key.png) | 灾厄试炼之匙 | 原生新绘 | 3 |
| [title_summit.png](art/title_summit.png) | 登顶者 | 原生新绘 | 3 |
| [forbidden_fruit.png](art/forbidden_fruit.png) | 禁果 | 原生新绘 | 7 |
| [blood_mud.png](art/blood_mud.png) | 血泥 | 原生新绘 | 5 |
| [broken_feather.png](art/broken_feather.png) | 断羽 | 原生新绘 | 4 |
