# 新老战友的幻影：从 idle 第一帧开始，记下当前位置。
scoreboard players set @s rpg_slgm_anim 0
scoreboard players set @s rpg_slgm_t 0
scoreboard players set @s rpg_slgm_mv 0
scoreboard players set @s rpg_slgm_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score @s rpg_slgm_x run data get storage rpg:display_mob pos[0] 100
execute store result score @s rpg_slgm_z run data get storage rpg:display_mob pos[2] 100
