# 失乐园建筑的来源

作者：**Boulevardier**（文件里的署名写作 BouJlevardier），作品发布在 Planet Minecraft（https://www.planetminecraft.com/）。
由仓库作者下载并提供；据其说明，这是公开免费的地图作品，使用时署名即可。作品页链接待补。

| 本包里的结构 | 用在 | 作品 | 原文件 |
|---|---|---|---|
| `rpg:paradise/eden_gate` | 伊甸之门 | Boulevardier's Archway Pack | Boulevardier's_Large_Archway.litematic |
| `rpg:paradise/tower_small` `tower_medium` `tower_big` `tower_large` | 四座河庭的塔 | Boulevardier's Primitive Structures Pack | Boulevardier's_Primitive_Tower_(small / medium / big / large).litematic |
| `rpg:paradise/house_small` `house_medium` `house_large` | 四座河庭的屋 | 同上 | Boulevardier's_Primitive_House_(small / medium / large).litematic |

改动（`_tools/add_eden_gate.py`）：
- 大门：苔石换泥砖，绿与紫的蛙明灯换成赭黄，亭台底下的空腔填实。
- 塔与屋：原样照搬，只把脚下悬空、会掉下来的沙砾与混凝土粉末换成同色实心方块；放进游戏后另开门洞、加光明方块与祭坛（祭坛是本包自己的）。

原始 litematic 不在仓库里（`.gitignore`），仓库只有转换后的结构。
