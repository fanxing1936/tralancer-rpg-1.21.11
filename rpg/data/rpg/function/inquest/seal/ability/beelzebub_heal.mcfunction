# 吞噬残魂：档位越高回得越多。
#
# 原本这里写的是 `regeneration 12t/18t/24t/36t 3`，算得很准 ——
# 再生 IV 每 6 刻跳一次，那四个时长正好回 2/3/4/6 点，严丝合缝对上
# 1x / 1.5x / 2x / 3x 的曲线。**但 `effect give` 的时长只收整数秒**，
# `t` 后缀是 `/time` 与 `schedule` 的语法。带 t 的那一版服务器会
# 拒绝加载整个函数，而 validate 抓不到（见 check_effect_duration.py）。
#
# 整秒粒度下精确的 2/3/4/6 表达不出来，所以改成调等级、保住"越躁动
# 回得越多"的形状：约 1 / 3 / 6 / 13 点。**这条待实机重新配平** ——
# 临界档 13 点偏高，但保持单调递增比凑准数字要紧。
execute if score @s rpg_agit matches 0..39 run effect give @s minecraft:regeneration 1 2 true
execute if score @s rpg_agit matches 40..69 run effect give @s minecraft:regeneration 1 3 true
execute if score @s rpg_agit matches 70..89 run effect give @s minecraft:regeneration 1 4 true
execute if score @s rpg_agit matches 90..99 run effect give @s minecraft:regeneration 2 4 true
scoreboard players add @s rpg_agit 3
execute if score @s rpg_agit matches 101.. run scoreboard players set @s rpg_agit 100
