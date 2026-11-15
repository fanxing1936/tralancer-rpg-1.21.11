# 一招结束：回到自由状态。
scoreboard players set @s rpg_l2_st 2
scoreboard players set @s rpg_l2_sk 0
scoreboard players set @s rpg_l2_t 0
attribute @s minecraft:movement_speed modifier remove rpg:lu2f_hold
attribute @s minecraft:armor modifier remove rpg:lu2f_open
tag @e[tag=rpg.unit] remove rpg.lu2f.hit
