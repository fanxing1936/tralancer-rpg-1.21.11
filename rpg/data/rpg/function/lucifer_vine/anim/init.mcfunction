# 新藤蔓：从 idle 第一帧开始，记下当前位置。
scoreboard players set @s rpg_luv_anim 0
scoreboard players set @s rpg_luv_t 0
scoreboard players set @s rpg_luv_mv 0
scoreboard players set @s rpg_luv_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score @s rpg_luv_x run data get storage rpg:display_mob pos[0] 100
execute store result score @s rpg_luv_z run data get storage rpg:display_mob pos[2] 100
