# 只管理司祭真实召唤的恼鬼，不按距离猜测主人，也不计入回廊敌人数。
# 先识别归属（含死亡动画中的主人），再检查主人是否存活。
execute unless entity @s[type=minecraft:vex] run return 0
scoreboard players set @s rpg_mn_tick 0
execute store success score @s rpg_mn_tick on origin if entity @s[tag=rpg.demon.minion,scores={rpg_mn_role=3}]
execute if score @s rpg_mn_tick matches 1 run tag @s add rpg.demon.minion.ritual_vex
execute unless entity @s[tag=rpg.demon.minion.ritual_vex] run return 0
scoreboard players set @s rpg_mn_tick 0
execute store success score @s rpg_mn_tick on origin if entity @s[tag=rpg.demon.minion,scores={rpg_mn_role=3},nbt={DeathTime:0s}] unless entity @s[nbt={Health:0.0f}]
execute if score @s rpg_mn_tick matches 0 run kill @s
