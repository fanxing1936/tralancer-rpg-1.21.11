# 新巨型空心人：从 idle 第一帧开始，记下当前位置。
scoreboard players set @s rpg_tw_m11_anim 0
scoreboard players set @s rpg_tw_m11_t 0
scoreboard players set @s rpg_tw_m11_mv 0
scoreboard players set @s rpg_tw_m11_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score @s rpg_tw_m11_x run data get storage rpg:display_mob pos[0] 100
execute store result score @s rpg_tw_m11_z run data get storage rpg:display_mob pos[2] 100
