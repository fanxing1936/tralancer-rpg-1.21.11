# 司祭 AI 一次性迁移：旧实体恢复寻路；仅修复为零的基础移速，不覆盖非零自定义速度或属性修饰器。
execute unless entity @s[type=minecraft:evoker,tag=rpg.demon.minion,scores={rpg_mn_role=3}] run return 0
data merge entity @s {NoAI:0b}
execute store result score #ritual_speed rpg_mn_tick run attribute @s minecraft:movement_speed base get 1000000
execute if score #ritual_speed rpg_mn_tick matches 0 run attribute @s minecraft:movement_speed base set 0.28
tag @s add rpg.demon.minion.ai_v1
