# 每 4 刻一次（as 载体）：比较这次和上次的位置。
scoreboard players set @s rpg_prlu_mc 0
data modify storage rpg:display_mob pos set from entity @s Pos
execute store result score #x rpg_prlu run data get storage rpg:display_mob pos[0] 100
execute store result score #z rpg_prlu run data get storage rpg:display_mob pos[2] 100
scoreboard players operation #dx rpg_prlu = #x rpg_prlu
scoreboard players operation #dx rpg_prlu -= @s rpg_prlu_x
scoreboard players operation #dz rpg_prlu = #z rpg_prlu
scoreboard players operation #dz rpg_prlu -= @s rpg_prlu_z
scoreboard players operation @s rpg_prlu_x = #x rpg_prlu
scoreboard players operation @s rpg_prlu_z = #z rpg_prlu
scoreboard players operation #dx rpg_prlu *= #dx rpg_prlu
scoreboard players operation #dz rpg_prlu *= #dz rpg_prlu
scoreboard players operation #dx rpg_prlu += #dz rpg_prlu
execute store success score @s rpg_prlu_mv if score #dx rpg_prlu matches 64..
