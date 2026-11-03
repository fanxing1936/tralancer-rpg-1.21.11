# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_vg_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_vg run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_vg run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_vg = #x rpg_vg
scoreboard players operation #dx rpg_vg -= @s rpg_vg_x
scoreboard players operation #dz rpg_vg = #z rpg_vg
scoreboard players operation #dz rpg_vg -= @s rpg_vg_z
scoreboard players operation @s rpg_vg_x = #x rpg_vg
scoreboard players operation @s rpg_vg_z = #z rpg_vg
scoreboard players operation #dx rpg_vg *= #dx rpg_vg
scoreboard players operation #dz rpg_vg *= #dz rpg_vg
scoreboard players operation #dx rpg_vg += #dz rpg_vg
execute store success score @s rpg_vg_mv if score #dx rpg_vg matches 64..
