# 新圣卫：盾满，冲锋冷却错开，免得一队人同时起步。
scoreboard players set @s rpg_tg_st 0
scoreboard players set @s rpg_tg_ta 0
scoreboard players set @s rpg_tg_cd 0
scoreboard players set @s rpg_tg_sh 6
execute store result score @s rpg_tg_cc run random value 40..120
