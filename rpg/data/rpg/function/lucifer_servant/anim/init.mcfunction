# 新路西法罪仆：从 idle 第一帧开始，记下当前位置。
scoreboard players set @s rpg_lcs_anim 0
scoreboard players set @s rpg_lcs_t 0
scoreboard players set @s rpg_lcs_mv 0
scoreboard players set @s rpg_lcs_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score @s rpg_lcs_x run data get storage rpg:display_mob pos[0] 100
execute store result score @s rpg_lcs_z run data get storage rpg:display_mob pos[2] 100
