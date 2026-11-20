# 新米迦勒灵体：从 idle 第一帧开始，记下当前位置。
scoreboard players set @s rpg_mis_anim 0
execute if entity @s[tag=rpg.michael_spirit.dual_rib] run scoreboard players set @s rpg_mis_anim 6
scoreboard players set @s rpg_mis_t 0
scoreboard players set @s rpg_mis_mv 0
scoreboard players set @s rpg_mis_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score @s rpg_mis_x run data get storage rpg:display_mob pos[0] 100
execute store result score @s rpg_mis_z run data get storage rpg:display_mob pos[2] 100
