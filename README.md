# 破碎大陆 · Eretz Ha-Shevarim

> אֶרֶץ הַשְּׁבָרִים ｜ 碎片之地
>
> 这是破碎大陆的见证：世界曾经完整，后来因神陨、堕天与权柄的分裂而成为碎片。

一套 Minecraft **Java 版 1.21.11** 的 RPG 内容组合：数据包 + 材质包 + 一份完整图鉴。
世界观全文见 [`LORE.md`](LORE.md)，图鉴里也整合了同一份叙事。
原作是 1.21 版本，本仓库是它的 1.21.11 升级版，并在升级过程中做了性能重构与内容扩充。

数据包格式 `94.1`，资源包格式 `75.0`（取自 `1.21.11-Fabric.jar` 的 `version.json`）。

---

## 内容

| 路径 | 说明 |
| --- | --- |
| `rpg/` | 数据包 —— 放进 `存档/datapacks/` |
| `resourcepack/` | 材质包 —— 放进 `.minecraft/resourcepacks/` |
| `rpg-datapack-1.21.11.zip` | 数据包 zip（同内容，方便分发） |
| `rpg-resourcepack-1.21.11.zip` | 材质包 zip |
| `TRALANCER-RPG-图鉴.html` | **图鉴**，双击即可打开 |
| `LORE.md` | **《破碎大陆》世界观全文**（圣经体叙事，七卷） |
| `ENGINEERING.md` | **完整工程日志**（十四部分，含每一处改动的原因与验证） |
| `_orig/` `_orig_rp/` | 原始 1.21 数据包 / 材质包备份，未改动 |
| `_tools/` | 迁移、优化、校验、打包、无头测试脚本 |

## 安装

1. 数据包放进存档的 `datapacks/`，材质包放进 `resourcepacks/` 并在游戏里启用。
2. 进入世界。计分板会由 `#minecraft:load` 自动建好，**不需要**再手动跑
   `function rpg:command/soreboard`。
3. 取装备：

```
/function rpg:command/give/box
```

一次给出 6 只潜影盒，装着全部 109 件武器、道具、升级材料与新锻装备。
（想逐件取仍可用 `give/weapon`、`give/item`、`give/weapon_up_item`、`give/extra`。）

## 内容概览

* **26 件武器**：剑、斧、弓、弩、重锤、长枪，分勇者 / 史诗 / 传说 / 恶魔 / 神圣五档
* **五位恶魔**：亚巴顿、别西卜、萨麦尔、贝利尔、**路西法**（长枪，主动技能［原罪］）
* **圣殿双柱**：雅斤与波阿斯，左右手双持触发联动
* **14 件护甲**、12 种药水、符文、镶嵌石、磨刀石与武器升级树
* **生物图鉴**：四大阵营，僵尸 / 骷髅 / 苦力怕出生时随机换装本包战利品

全部条目连同**按游戏内真实合成的图标**（染色、盔甲纹饰、药水颜色、附魔光泽）
都在 `TRALANCER-RPG-图鉴.html` 里。

## 重建

```bash
bash _tools/build.sh          # 数据包
bash _tools/rp_build.sh       # 材质包
bash _tools/guide_build.sh    # 图鉴
python _tools/package.py --install
```

两个包都是**从 `_orig/` `_orig_rp/` 的原始 1.21 副本重新生成的**，不是手工改的 ——
任何修改都应该改 `_tools/` 里对应的生成脚本，而不是改输出。

验证手段：`_tools/server_test.py` 会用客户端 jar 起一个真实的 1.21.11 无头服务器加载数据包，
`validate.py` / `rp_validate.py` 对着同一个 jar 校验两个包。

## 致谢

原始 RPG 内容、全部美术与世界观设定：**仓库作者**。

1.21.11 迁移、性能重构、图鉴生成、以及路西法与圣殿双柱等新增内容：
与 **Claude**（Anthropic）结对完成 —— 逐轮讨论、实现、在真实服务器上验证。

过程中的每一个判断、每一处踩坑与修正，都记在 [`ENGINEERING.md`](ENGINEERING.md) 里。

感谢这段合作。
