# 新先锋罪仆：从 idle 第一帧开始，记下当前位置。
scoreboard players set @s rpg_vg_anim 0
scoreboard players set @s rpg_vg_t 0
scoreboard players set @s rpg_vg_mv 0
execute store result score @s rpg_vg_x run data get entity @s Pos[0] 100
execute store result score @s rpg_vg_z run data get entity @s Pos[2] 100
