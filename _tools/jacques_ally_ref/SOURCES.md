# 来源

从《Minecraft Dungeons》本体提取（只读），由 `make_oath_icon.py` 渲染成圣殿誓约的物品贴图 `oath.png`（32×32）。

- 风之号角（Wind Horn）：`Dungeons/Content/Actors/Items/WindHorn/`
  - `SM_WindHorn`：号角网格（190 个三角面，方块拼成）
  - `T_Windhorn.png`（32×32）：网格的像素贴图，十几种平涂色
  - `T_WindHorn_Icon_inventory.png`：原作物品图标，只用来对角度
- 做法：贴图逐像素换成圣殿配色，按原作图标的角度（偏航 -60°、俯仰 -25°、画面内 40°）正交投影，8 倍超采样后每格取多数色，面按朝向分三档明暗，外圈加深色描边。

版权归 Mojang 所有；本项目非商业，与 Mojang 无关联。
