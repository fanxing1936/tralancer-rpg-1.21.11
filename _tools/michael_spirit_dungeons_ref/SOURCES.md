# 米迦勒灵体模型

- 人物沿用《Minecraft Dungeons》的 `SK_Player_Master` 骨架和身体网格。原作外观表的 `CloudWatcher` 行使用 `MI_Nephrologist` 和 `T_Nephrologist_Skin`。
- 霜冻护甲取自 `SnowArmor_Unique1`。使用 `BP_SnowArmor_Unique1` 的六件静态网格、骨架插槽和相对变换。
- 米迦勒脊骨和米迦勒肋骨来自 TRA 现有两把武器的手持贴图，以原像素轮廓生成带厚度的模型，并挂到原作英雄的武器插槽上。
- 动作来源和时长见 `model_config.json` 的 `clips`。单持版右手拿脊骨，使用原作长柄武器待机、移动和三连。双持版左右手各拿一把肋骨，使用原作英雄待机和移动、双匕首六段连击。两版按各自固定持武播放，共用原作翻滚、受伤和倒地动作。
- 皮肤是近白色 `#FFF5EE`，武器是橙红色 `#FF3300`。霜冻护甲保留原图明暗，用 `#FF3300`、`#FF805F`、`#FFD0BD` 区分阴影、中间色和高光。所有贴图半透明，并保留原图镂空。

在《Minecraft Java 1.21.11》同时安装当前 TRA 数据包和材质包后，可以用 `/function rpg:michael_spirit/debug/preview_spine` 召出单持脊骨版，用 `/function rpg:michael_spirit/debug/preview_dual_rib` 召出双肋骨版。用 `/function rpg:michael_spirit/debug/play/slash1` 或 `/function rpg:michael_spirit/debug/play/rib_slash1` 播放对应动作，用 `/function rpg:michael_spirit/debug/clear` 清除预览。其他动作的命令尾段与 `model_config.json` 中的动作 ID 相同。

场景可以为载体使用 `rpg.michael_spirit.carrier` 标签，并在召唤时给出 `rpg.michael_spirit.spine` 或 `rpg.michael_spirit.dual_rib` 标签。载体可作为执行者调用 `rpg:michael_spirit/play/<动作ID>`。模型每刻跟随载体的位置和朝向，走停自动切换对应的待机和步行动作。去掉载体标签可解除模型。两件玩家可领取装备继续使用既有物品定义，灵体使用专用显示模型。

用 `_tools/convert_michael_spirit.py <原作导出工作目录>` 可重建转换模型，输入为解包的 UModel glTF、Frost Armor 和长柄武器蓝图、原作玩家骨骼及动作轨道，以及从 TRA 贴图转换的两把武器。提供 `--source` 可指定原作轨道与骨骼导出根目录。`_tools/add_michael_spirit_model.py` 从此目录的 `.bbmodel` 和配置生成 Java 资源与动作函数，由两份正式构建脚本调用。
