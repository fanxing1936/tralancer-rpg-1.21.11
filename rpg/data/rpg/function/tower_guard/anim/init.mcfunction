# 新圣卫：从 idle 第一帧开始，记下当前位置。
scoreboard players set @s rpg_tg_anim 0
scoreboard players set @s rpg_tg_t 0
scoreboard players set @s rpg_tg_mv 0
execute store result score @s rpg_tg_x run data get entity @s Pos[0] 100
execute store result score @s rpg_tg_z run data get entity @s Pos[2] 100
