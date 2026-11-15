# 新圣卫·重盾：从 idle 第一帧开始，记下当前位置。
scoreboard players set @s rpg_rg_anim 0
scoreboard players set @s rpg_rg_t 0
scoreboard players set @s rpg_rg_mv 0
scoreboard players set @s rpg_rg_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score @s rpg_rg_x run data get storage rpg:display_mob pos[0] 100
execute store result score @s rpg_rg_z run data get storage rpg:display_mob pos[2] 100
